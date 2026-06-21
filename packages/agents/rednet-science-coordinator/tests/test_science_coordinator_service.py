from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


SERVICE_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "science_coordinator_service.py"
)
SCHEMA_PATH = Path(__file__).resolve().parents[4] / "schemas" / "science-flow.schema.json"
MANIFEST_PATH = Path(__file__).resolve().parents[1] / "manifest.json"

spec = importlib.util.spec_from_file_location("science_coordinator_service", SERVICE_PATH)
service = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(service)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    assert isinstance(data, dict)
    return data


class ScienceCoordinatorServiceTests(unittest.TestCase):
    def test_status_is_read_only(self) -> None:
        manifest = {
            "id": "rednet-science-coordinator",
            "version": "0.2.0",
            "status": "template",
            "default_mode": "observe",
            "allowed_modes": ["off", "observe", "assisted", "guided"],
            "forbidden_modes_by_default": ["lab-active", "trusted-lab"],
            "flows": ["papers", "concepts"],
            "required_artifacts": ["task_card"],
            "guards": {
                "live_commands": False,
                "network_changes": False,
                "docker_control": False,
                "artifact_required": True,
            },
        }
        status = service.build_status(manifest, [], {"REDNET_AGENT_MODE": "observe"})
        self.assertTrue(status["ok"])
        self.assertEqual(status["mode"], "observe")
        self.assertFalse(status["invalid_mode"])
        self.assertFalse(status["live_commands"])
        self.assertFalse(status["network_changes"])
        self.assertFalse(status["docker_control"])
        self.assertTrue(status["artifact_required"])

    def test_forbidden_mode_falls_back_to_safe_default(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        status = service.build_status(
            manifest,
            [],
            {"REDNET_AGENT_MODE": "lab-active"},
        )
        self.assertEqual(status["mode"], "observe")
        self.assertEqual(status["requested_mode"], "lab-active")
        self.assertTrue(status["invalid_mode"])
        self.assertIn("lab-active", status["forbidden_modes_by_default"])
        self.assertFalse(status["live_commands"])

    def test_environment_does_not_expose_auth_reference(self) -> None:
        env = {
            "REDNET_MODEL_AUTH_REF": "private-value",
            "REDNET_MODEL_NAME": "example-model",
        }
        safe = service.safe_environment(env)
        self.assertNotIn("REDNET_MODEL_AUTH_REF", safe)
        self.assertTrue(safe["REDNET_MODEL_AUTH_REF_PRESENT"])
        self.assertEqual(safe["REDNET_MODEL_NAME"], "example-model")

    def test_example_ledger_is_jsonl_objects(self) -> None:
        rows = service.load_jsonl(service.EXAMPLE_LEDGER_PATH)
        self.assertGreaterEqual(len(rows), 2)
        self.assertTrue(all(isinstance(row, dict) for row in rows))
        self.assertTrue(all("id" in row for row in rows))

    def test_tasks_endpoint_has_no_private_fields(self) -> None:
        code, payload = service.response_for_path("/tasks")
        self.assertEqual(code, 200)
        encoded = json.dumps(payload, ensure_ascii=False).lower()
        self.assertNotIn("token", encoded)
        self.assertNotIn("oauth", encoded)
        self.assertNotIn("telegram", encoded)

    def test_read_only_endpoints(self) -> None:
        for path in ("/", "/health", "/status", "/flows", "/tasks"):
            with self.subTest(path=path):
                code, payload = service.response_for_path(path)
                self.assertEqual(code, 200)
                self.assertTrue(payload["ok"])
        code, payload = service.response_for_path("/missing")
        self.assertEqual(code, 404)
        self.assertFalse(payload["ok"])

    def test_manifest_matches_science_flow_schema_enums(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        schema = load_json(SCHEMA_PATH)
        flow_enum = set(schema["properties"]["flow"]["enum"])
        artifact_enum = set(schema["properties"]["artifact"]["enum"])
        self.assertEqual(set(manifest["flows"]), flow_enum)
        self.assertEqual(set(manifest["required_artifacts"]), artifact_enum)

    def test_example_ledger_matches_schema_contract(self) -> None:
        schema = load_json(SCHEMA_PATH)
        required = set(schema["required"])
        id_pattern = re.compile(schema["properties"]["id"]["pattern"])
        enums = {
            key: set(value["enum"])
            for key, value in schema["properties"].items()
            if isinstance(value, dict) and "enum" in value
        }
        for row in service.load_jsonl(service.EXAMPLE_LEDGER_PATH):
            with self.subTest(row=row["id"]):
                self.assertTrue(required <= set(row))
                self.assertRegex(row["id"], id_pattern)
                for key, allowed in enums.items():
                    if key in row:
                        self.assertIn(row[key], allowed)


if __name__ == "__main__":
    unittest.main()
