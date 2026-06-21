from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import closing
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "airin_neural_service_node.py"


def load_runtime(temp_localappdata: str):
    old = os.environ.get("LOCALAPPDATA")
    os.environ["LOCALAPPDATA"] = temp_localappdata
    try:
        spec = importlib.util.spec_from_file_location("airin_neural_service_node_under_test", SCRIPT)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        if old is None:
            os.environ.pop("LOCALAPPDATA", None)
        else:
            os.environ["LOCALAPPDATA"] = old


class Stage1AdviseTests(unittest.TestCase):
    def test_init_creates_stage1_tables_idempotently(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            mod.load_config()
            mod.connect_db().close()
            mod.connect_db().close()

            with closing(sqlite3.connect(mod.DB_PATH)) as conn:
                tables = {row[0] for row in conn.execute("select name from sqlite_master where type='table'")}

            self.assertTrue(
                {
                    "assessments",
                    "service_state",
                    "node_events",
                    "node_assessments",
                    "node_recommendations",
                    "node_feedback",
                    "attempt_patterns",
                }.issubset(tables)
            )

    def test_advise_mode_records_pending_recommendation_without_actions(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            mod.set_mode("advise", "unit test stage 1")

            mod.collect_module_status = lambda: {
                "ok": True,
                "hermes_launch_survival": {
                    "mode": "hold",
                    "task_installed": True,
                    "process_counts": {"gateway": 1, "packaged_desktop": 0},
                },
                "warnings": [],
            }
            mod.call_lmstudio = lambda compact, cfg: (
                True,
                {
                    "state": "telegram_degraded",
                    "severity": "warning",
                    "confidence": 0.73,
                    "evidence": ["gateway_alive", "telegram_timeout"],
                    "recommendation": "hold_queue_and_use_local_chat",
                    "forbidden": ["reset_gateway"],
                    "notes": "advise only",
                },
                "{}",
            )

            result = mod.assess(types.SimpleNamespace(source="unit-test"))

            self.assertTrue(result["ok"])
            self.assertEqual(result["mode"], "advise")
            self.assertIn("advice", result)
            self.assertEqual(result["advice"]["status"], "pending")
            self.assertFalse(result["advice"]["action_allowed"])

            with closing(sqlite3.connect(mod.DB_PATH)) as conn:
                row = conn.execute(
                    "select recommendation, status, action_allowed from node_recommendations order by created_at desc limit 1"
                ).fetchone()

            self.assertEqual(row, ("hold_queue_and_use_local_chat", "pending", 0))

    def test_secret_like_evidence_is_redacted_before_storage(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            normalized = mod.normalize_assessment(
                {
                    "state": "probe",
                    "severity": "normal",
                    "confidence": 0.9,
                    "evidence": [
                        "gateway_alive",
                        "Authorization = demo-marker",
                        "password=hunter2",
                        "candidate sk-demo-leak",
                    ],
                    "recommendation": "observe",
                },
                mod.load_config(),
            )

            joined = "\n".join(normalized["evidence"])
            self.assertIn("gateway_alive", joined)
            self.assertNotIn("demo-marker", joined)
            self.assertNotIn("hunter2", joined)
            self.assertNotIn("sk-demo-leak", joined)
            self.assertIn("[redacted-secret-like-evidence]", joined)

    def test_advise_cli_creates_pending_recommendation_without_changing_persistent_mode(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            cfg = mod.load_config()
            cfg["enabled"] = False
            cfg["mode"] = "observe"
            mod.save_config(cfg)

            env = os.environ.copy()
            env["LOCALAPPDATA"] = tmp
            env["PYTHONUTF8"] = "1"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "advise", "--source", "unit-cli"],
                env=env,
                capture_output=True,
                text=True,
                timeout=20,
                encoding="utf-8",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            result = json.loads(completed.stdout)
            self.assertTrue(result["ok"])
            self.assertEqual(result["mode"], "advise")
            self.assertEqual(result["advice"]["status"], "pending")
            self.assertFalse(result["advice"]["action_allowed"])

            persisted = json.loads(mod.CONFIG_PATH.read_text(encoding="utf-8"))
            self.assertEqual(persisted["mode"], "observe")

            with closing(sqlite3.connect(mod.DB_PATH)) as conn:
                row = conn.execute(
                    "select source, status, action_allowed from node_recommendations order by created_at desc limit 1"
                ).fetchone()
            self.assertEqual(row, ("unit-cli", "pending", 0))


    def test_stage1_act_mode_still_blocks_actions(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            cfg = mod.load_config()
            cfg["enabled"] = False
            cfg["mode"] = "act"
            cfg["allow_actions"] = True
            mod.save_config(cfg)

            mod.collect_module_status = lambda: {
                "ok": True,
                "hermes_launch_survival": {
                    "mode": "hold",
                    "task_installed": True,
                    "process_counts": {"gateway": 1, "packaged_desktop": 0},
                },
                "warnings": [],
            }

            result = mod.assess(types.SimpleNamespace(source="unit-act"))

            self.assertTrue(result["ok"])
            self.assertEqual(result["mode"], "act")
            self.assertEqual(result["advice"]["status"], "blocked")
            self.assertFalse(result["advice"]["action_allowed"])

            with closing(sqlite3.connect(mod.DB_PATH)) as conn:
                row = conn.execute(
                    "select status, action_allowed, reason from node_recommendations order by created_at desc limit 1"
                ).fetchone()
            self.assertEqual(row, ("blocked", 0, "stage1_advise_only_no_action_execution"))

    def test_lmstudio_endpoint_must_be_loopback(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            cfg = mod.load_config()
            cfg["lmstudio_base_url"] = "https://example.com/v1"

            health = mod.lmstudio_health(cfg)
            ok, model_result, raw = mod.call_lmstudio({}, cfg)

            self.assertFalse(health["ok"])
            self.assertEqual(health["error"], "non_loopback_lmstudio_base_url")
            self.assertFalse(ok)
            self.assertEqual(model_result["error"], "non_loopback_lmstudio_base_url")
            self.assertEqual(raw, "")

    def test_storage_redacts_secret_like_compact_result_and_raw(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            mod = load_runtime(tmp)
            cfg = mod.load_config()
            compact = {
                "ok": True,
                "warnings": ["Authorization = demo-marker", "candidate sk-demo-leak"],
            }
            result = mod.normalize_assessment(
                {
                    "state": "probe",
                    "severity": "normal",
                    "confidence": 0.9,
                    "evidence": ["passwd=hunter2"],
                    "recommendation": "observe",
                    "notes": "candidate sk-demo-leak",
                },
                cfg,
            )

            mod.store_assessment("unit-storage", compact, result, "passwd=hunter2\ncandidate sk-demo-leak", False, cfg)

            with closing(sqlite3.connect(mod.DB_PATH)) as conn:
                row = conn.execute(
                    """
                    select e.event_json, a.input_json, a.result_json, a.raw_response, n.assessment_json
                    from assessments a
                    join node_events e on e.id = (select event_id from node_assessments where id = a.id)
                    join node_assessments n on n.id = a.id
                    order by a.created_at desc limit 1
                    """
                ).fetchone()

            joined = "\n".join(row)
            self.assertNotIn("demo-marker", joined)
            self.assertNotIn("hunter2", joined)
            self.assertNotIn("sk-demo-leak", joined)
            self.assertIn("[redacted-secret-like-evidence]", joined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
