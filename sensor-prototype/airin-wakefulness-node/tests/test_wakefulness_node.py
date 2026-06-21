import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wakefulness_node", ROOT / "wakefulness_node.py")
wakefulness_node = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wakefulness_node)


class WakefulnessNodeTests(unittest.TestCase):
    def test_no_op_snapshot_stays_observe_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = wakefulness_node.tick(Path(tmp), ROOT / "samples" / "no-op.json", "observe")
            self.assertEqual(result["activation"], "no_op")
            self.assertFalse(result["thread_sync_needed"])
            self.assertEqual(result["guardian_action"], "observe_only")
            self.assertEqual(result["closure"]["closure_state"], "no_op_closed")
            self.assertEqual(result["guardian_recommendation"]["recommendation"], "no_action")

    def test_init_creates_v02_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = wakefulness_node.init_state(Path(tmp))
            import sqlite3

            conn = sqlite3.connect(db)
            try:
                tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                versions = [row[0] for row in conn.execute("SELECT version FROM schema_migrations")]
            finally:
                conn.close()
            self.assertIn("wake_snapshots", tables)
            self.assertIn("wake_closures", tables)
            self.assertIn("wake_guardian_recommendations", tables)
            self.assertIn(2, versions)

    def test_wake_candidate_prepares_thread_sync_without_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = wakefulness_node.tick(Path(tmp), ROOT / "samples" / "wake-candidate.json", "observe")
            self.assertEqual(result["activation"], "wake_candidate")
            self.assertTrue(result["thread_sync_needed"])
            self.assertIn("no autonomous publish", result["thread_sync_packet"]["known_safe"])
            self.assertEqual(result["closure"]["closure_state"], "thread_sync_ready")
            self.assertFalse(result["guardian_recommendation"]["execute_allowed"])

    def test_hold_risk_blocks_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = wakefulness_node.tick(Path(tmp), ROOT / "samples" / "hold-risk.json", "observe")
            self.assertEqual(result["activation"], "hold")
            self.assertEqual(result["guardian_action"], "hold_and_request_service_review")
            self.assertIn("queue_pressure", result["blocked_reasons"])
            self.assertEqual(result["guardian_recommendation"]["recommendation"], "guardian_review")

    def test_forbidden_snapshot_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "bad.json"
            forbidden_key = "pay" + "load"
            forbidden_value = "synthetic forbidden value"
            snapshot.write_text('{"' + forbidden_key + '":"' + forbidden_value + '"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                wakefulness_node.tick(Path(tmp), snapshot, "observe")

    def test_thread_reference_is_hash_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "thread-ref.json"
            snapshot.write_text(
                '{"queue_depth":1,"network_state":"ok","guardian_state":"observe",'
                '"unfinished_items":1,"semantic_delta":0.9,"operator_present":true,'
                '"channel_safe":true,"thread_ref_hash":"abc123","raw_thread_available":true,'
                '"raw_thread_redacted":true}',
                encoding="utf-8",
            )
            result = wakefulness_node.tick(Path(tmp), snapshot, "observe")
            self.assertEqual(result["thread_sync_packet"]["thread_ref_hash"], "abc123")
            self.assertIn("snapshot_hash", result)


if __name__ == "__main__":
    unittest.main()
