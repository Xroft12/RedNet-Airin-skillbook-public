import json
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sensor", ROOT / "sensor.py")
sensor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sensor)


class SensorTests(unittest.TestCase):
    def test_init_creates_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = sensor.init_state(Path(tmp))
            self.assertTrue(db.exists())
            conn = sqlite3.connect(db)
            try:
                tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            finally:
                conn.close()
            self.assertIn("sensor_events", tables)
            self.assertIn("guardian_recommendations", tables)

    def test_ingest_redacts_payload_and_creates_assessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            replay = Path(tmp) / "synthetic-payload-check.jsonl"
            forbidden_key = "pay" + "load"
            forbidden_value = "synthetic forbidden value"
            replay.write_text(json.dumps({
                "timestamp": "2026-06-07T09:15:00Z",
                "event_type": "weird",
                "proto": "udp",
                "src_ip": "192.0.2.15",
                "dest_ip": "203.0.113.200",
                "src_port": 62000,
                "dest_port": 49152,
                "bytes_toserver": 20,
                "bytes_toclient": 0,
                "duration": 0.0,
                forbidden_key: forbidden_value,
            }) + "\n", encoding="utf-8")
            result = sensor.ingest_replay(Path(tmp), replay)
            self.assertEqual(result["total"], 1)
            db = sensor.db_path(Path(tmp))
            raw = db.read_bytes()
            self.assertNotIn(forbidden_value.encode("utf-8"), raw)
            conn = sqlite3.connect(db)
            try:
                count = conn.execute("SELECT COUNT(*) FROM sensor_assessments").fetchone()[0]
            finally:
                conn.close()
            self.assertEqual(count, 1)

    def test_dns_fail_becomes_degraded(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = sensor.ingest_replay(Path(tmp), ROOT / "samples" / "dns-fail.jsonl")
            self.assertGreaterEqual(result["degraded"], 1)
            summary = sensor.assessment_summary(Path(tmp))
            self.assertEqual(summary["dominant_state"], "degraded")
            self.assertEqual(summary["safe_action"], "observe-only; no network/firewall/VPN action")

    def test_normal_flow_is_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = sensor.ingest_replay(Path(tmp), ROOT / "samples" / "normal-flow.jsonl")
            self.assertGreaterEqual(result["ok"], 1)
            summary = sensor.assessment_summary(Path(tmp))
            self.assertIn(summary["dominant_state"], {"ok", "empty"})


if __name__ == "__main__":
    unittest.main()
