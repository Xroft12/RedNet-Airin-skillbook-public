#!/usr/bin/env python3
"""Observe-only wakefulness node for REDNET Airin Skillbook."""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Tuple


ALLOWED_MODES = {"off", "observe", "feel", "service", "hold"}
SCHEMA_VERSION = 2
FORBIDDEN_FIELDS = {
    "payload",
    "message",
    "body",
    "content",
    "text",
    "token",
    "password",
    "session",
    "cookie",
    "audio",
    "transcript",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wake_ticks (
  tick_id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  mode TEXT NOT NULL,
  activation TEXT NOT NULL,
  confidence REAL NOT NULL,
  guardian_action TEXT NOT NULL,
  reason TEXT NOT NULL,
  thread_sync_needed INTEGER NOT NULL,
  snapshot_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wake_snapshots (
  snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER,
  created_at TEXT NOT NULL,
  snapshot_version TEXT NOT NULL,
  source_kind TEXT NOT NULL,
  poll_id TEXT NOT NULL,
  queue_depth INTEGER NOT NULL,
  queue_age_sec REAL NOT NULL,
  network_state TEXT NOT NULL,
  guardian_state TEXT NOT NULL,
  channel_safe INTEGER NOT NULL,
  operator_present INTEGER NOT NULL,
  unfinished_items INTEGER NOT NULL,
  semantic_delta REAL NOT NULL,
  risk_level TEXT NOT NULL,
  last_tick_age_sec REAL NOT NULL,
  last_activation TEXT NOT NULL,
  cooldown_active INTEGER NOT NULL,
  manual_wake_allowed INTEGER NOT NULL,
  thread_ref_hash TEXT NOT NULL,
  raw_thread_available INTEGER NOT NULL,
  raw_thread_redacted INTEGER NOT NULL,
  blocked_reasons_json TEXT NOT NULL,
  ttl_sec INTEGER NOT NULL,
  schema_hash TEXT NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);

CREATE TABLE IF NOT EXISTS thread_sync_packets (
  packet_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  packet_json TEXT NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);

CREATE TABLE IF NOT EXISTS wake_thread_refs (
  ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  thread_ref_hash TEXT NOT NULL,
  raw_thread_available INTEGER NOT NULL,
  raw_thread_redacted INTEGER NOT NULL,
  ttl_sec INTEGER NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);

CREATE TABLE IF NOT EXISTS wake_guardian_recommendations (
  recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  confidence REAL NOT NULL,
  execute_allowed INTEGER NOT NULL,
  reason TEXT NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);

CREATE TABLE IF NOT EXISTS wake_closures (
  closure_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  closure_state TEXT NOT NULL,
  next_tick_after_sec INTEGER NOT NULL,
  safe_to_sleep INTEGER NOT NULL,
  reason TEXT NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);

CREATE TABLE IF NOT EXISTS wake_policy (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wake_audit (
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tick_id INTEGER,
  created_at TEXT NOT NULL,
  event TEXT NOT NULL,
  details_json TEXT NOT NULL,
  FOREIGN KEY(tick_id) REFERENCES wake_ticks(tick_id)
);
"""


def db_path(state_dir: Path) -> Path:
    return state_dir / "wakefulness.sqlite3"


def init_state(state_dir: Path) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    db = db_path(state_dir)
    conn = sqlite3.connect(db)
    try:
        conn.executescript(SCHEMA)
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        conn.execute(
            "INSERT OR IGNORE INTO schema_migrations(version, applied_at, description) VALUES(?,?,?)",
            (SCHEMA_VERSION, now, "wakefulness node v0.2 observe-only schema"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO wake_policy(key, value, updated_at) VALUES(?,?,?)",
            ("mode_contract", "off/observe/feel/service/hold; no execute", now),
        )
        conn.execute(
            "INSERT OR IGNORE INTO wake_policy(key, value, updated_at) VALUES(?,?,?)",
            ("default_action", "no_op is a successful closure", now),
        )
        conn.commit()
    finally:
        conn.close()
    return db


def stable_hash(data: Dict[str, Any]) -> str:
    import hashlib

    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def assert_safe_snapshot(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_FIELDS:
                raise ValueError(f"forbidden field in snapshot: {path}.{key}")
            assert_safe_snapshot(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_safe_snapshot(child, f"{path}[{index}]")


def load_snapshot(path: Path) -> Dict[str, Any]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be a JSON object")
    assert_safe_snapshot(snapshot)
    return snapshot


def as_float(snapshot: Dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(snapshot.get(key, default))
    except (TypeError, ValueError):
        return default


def as_int(snapshot: Dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(snapshot.get(key, default))
    except (TypeError, ValueError):
        return default


def normalize_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    blocked_reasons = as_list(snapshot.get("blocked_reasons"))
    queue_depth = as_int(snapshot, "queue_depth")
    queue_age_sec = as_float(snapshot, "queue_age_sec")
    network_state = str(snapshot.get("network_state", "unknown")).lower()
    guardian_state = str(snapshot.get("guardian_state", "observe")).lower()
    channel_safe = bool(snapshot.get("channel_safe", True))
    operator_present = bool(snapshot.get("operator_present", False))
    unfinished_items = as_int(snapshot, "unfinished_items")
    semantic_delta = as_float(snapshot, "semantic_delta")
    risk_level = str(snapshot.get("risk_level", "none")).lower()
    cooldown_active = bool(snapshot.get("cooldown_active", False))
    manual_wake_allowed = bool(snapshot.get("manual_wake_allowed", True))
    raw_thread_available = bool(snapshot.get("raw_thread_available", False))
    raw_thread_redacted = bool(snapshot.get("raw_thread_redacted", True))

    if not channel_safe:
        blocked_reasons.append("unsafe_channel")
    if network_state in {"degraded", "down", "blocked"}:
        blocked_reasons.append(f"network_{network_state}")
    if guardian_state in {"hold", "incident"}:
        blocked_reasons.append(f"guardian_{guardian_state}")
    if queue_depth >= 100:
        blocked_reasons.append("queue_pressure")
    if queue_age_sec >= 600:
        blocked_reasons.append("queue_age")
    if risk_level in {"high", "critical"}:
        blocked_reasons.append(f"risk_{risk_level}")
    if cooldown_active:
        blocked_reasons.append("cooldown")
    if raw_thread_available and not raw_thread_redacted:
        blocked_reasons.append("raw_thread_not_redacted")

    normalized = {
        "snapshot_version": str(snapshot.get("snapshot_version", "0.2")),
        "source_kind": str(snapshot.get("source_kind", "manual-snapshot")),
        "poll_id": str(snapshot.get("poll_id", stable_hash(snapshot)[:16])),
        "queue_depth": queue_depth,
        "queue_age_sec": queue_age_sec,
        "network_state": network_state,
        "guardian_state": guardian_state,
        "channel_safe": channel_safe,
        "operator_present": operator_present,
        "unfinished_items": unfinished_items,
        "semantic_delta": semantic_delta,
        "risk_level": risk_level,
        "last_tick_age_sec": as_float(snapshot, "last_tick_age_sec", -1.0),
        "last_activation": str(snapshot.get("last_activation", "unknown")),
        "cooldown_active": cooldown_active,
        "manual_wake_allowed": manual_wake_allowed,
        "thread_ref_hash": str(snapshot.get("thread_ref_hash", "")),
        "raw_thread_available": raw_thread_available,
        "raw_thread_redacted": raw_thread_redacted,
        "blocked_reasons": sorted(set(blocked_reasons)),
        "ttl_sec": as_int(snapshot, "ttl_sec", 300),
    }
    normalized["schema_hash"] = stable_hash({
        "schema_version": SCHEMA_VERSION,
        "snapshot_fields": sorted(normalized.keys()),
    })
    return normalized


def has_blockers(snapshot: Dict[str, Any]) -> bool:
    return bool(snapshot.get("blocked_reasons"))


def closure_for(activation: str, reason: str) -> Dict[str, Any]:
    if activation == "hold":
        state = "held_for_guardian_review"
        next_tick = 30
        safe_to_sleep = False
    elif activation == "wake_candidate":
        state = "thread_sync_ready"
        next_tick = 10
        safe_to_sleep = False
    elif activation == "service_report":
        state = "diagnostics_ready"
        next_tick = 30
        safe_to_sleep = True
    elif activation == "feel":
        state = "soft_signal_stored"
        next_tick = 60
        safe_to_sleep = True
    else:
        state = "no_op_closed"
        next_tick = 120
        safe_to_sleep = True
    return {
        "closure_state": state,
        "next_tick_after_sec": next_tick,
        "safe_to_sleep": safe_to_sleep,
        "reason": reason,
    }


def recommendation_for(assessment: Dict[str, Any], snapshot: Dict[str, Any]) -> Dict[str, Any]:
    activation = assessment["activation"]
    if activation == "hold":
        recommendation = "guardian_review"
    elif activation == "wake_candidate":
        recommendation = "prepare_manual_wake"
    elif activation == "service_report":
        recommendation = "show_diagnostics"
    elif activation == "feel":
        recommendation = "keep_short_term_note"
    else:
        recommendation = "no_action"
    return {
        "recommendation": recommendation,
        "confidence": assessment["confidence"],
        "execute_allowed": False,
        "reason": "; ".join(snapshot.get("blocked_reasons", [])) or assessment["reason"],
    }


def evaluate_snapshot(snapshot: Dict[str, Any], mode: str) -> Tuple[Dict[str, Any], Dict[str, Any] | None]:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"unsupported mode: {mode}")

    queue_depth = int(snapshot["queue_depth"])
    unfinished_items = int(snapshot["unfinished_items"])
    semantic_delta = float(snapshot["semantic_delta"])
    network_state = str(snapshot["network_state"]).lower()
    guardian_state = str(snapshot["guardian_state"]).lower()
    channel_safe = bool(snapshot["channel_safe"])
    operator_present = bool(snapshot["operator_present"])
    manual_wake_allowed = bool(snapshot["manual_wake_allowed"])

    if mode == "off":
        activation = "off"
        confidence = 1.0
        action = "no_action"
        reason = "wakefulness cascade is off"
    elif mode == "hold" or has_blockers(snapshot):
        activation = "hold"
        confidence = 0.86
        action = "hold_and_request_service_review"
        reason = "risk, unsafe channel, degraded network, or queue pressure"
    elif mode == "service":
        activation = "service_report"
        confidence = 0.78
        action = "show_operator_diagnostics"
        reason = "service mode requested"
    elif semantic_delta >= 0.80 and operator_present and guardian_state in {"observe", "service"} and manual_wake_allowed:
        activation = "wake_candidate"
        confidence = min(0.95, 0.55 + semantic_delta / 2)
        action = "prepare_thread_sync_packet"
        reason = "meaningful semantic delta with safe channel and operator present"
    elif mode == "feel" or semantic_delta >= 0.45 or unfinished_items > 0:
        activation = "feel"
        confidence = min(0.82, 0.45 + max(semantic_delta, unfinished_items / 10))
        action = "store_passive_short_term_note"
        reason = "soft signal should be held without publication"
    else:
        activation = "no_op"
        confidence = 0.90
        action = "observe_only"
        reason = "no meaningful delta"

    thread_sync_needed = activation in {"wake_candidate", "hold", "service_report"}
    assessment = {
        "activation": activation,
        "confidence": round(confidence, 3),
        "guardian_action": action,
        "reason": reason,
        "thread_sync_needed": thread_sync_needed,
        "mode": mode,
        "blocked_reasons": snapshot["blocked_reasons"],
    }
    packet = None
    if thread_sync_needed:
        packet = {
            "why": reason,
            "activation": activation,
            "known_safe": ["no payload", "no autonomous publish", "no network action"],
            "blocked": ["direct publish", "durable memory write", "route change"],
            "next": action,
            "thread_ref_hash": snapshot["thread_ref_hash"],
            "ttl_sec": snapshot["ttl_sec"],
        }
    return assessment, packet


def insert_snapshot(conn: sqlite3.Connection, tick_id: int, now: str, snapshot: Dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO wake_snapshots(
          tick_id, created_at, snapshot_version, source_kind, poll_id, queue_depth, queue_age_sec,
          network_state, guardian_state, channel_safe, operator_present, unfinished_items,
          semantic_delta, risk_level, last_tick_age_sec, last_activation, cooldown_active,
          manual_wake_allowed, thread_ref_hash, raw_thread_available, raw_thread_redacted,
          blocked_reasons_json, ttl_sec, schema_hash
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            tick_id,
            now,
            snapshot["snapshot_version"],
            snapshot["source_kind"],
            snapshot["poll_id"],
            snapshot["queue_depth"],
            snapshot["queue_age_sec"],
            snapshot["network_state"],
            snapshot["guardian_state"],
            1 if snapshot["channel_safe"] else 0,
            1 if snapshot["operator_present"] else 0,
            snapshot["unfinished_items"],
            snapshot["semantic_delta"],
            snapshot["risk_level"],
            snapshot["last_tick_age_sec"],
            snapshot["last_activation"],
            1 if snapshot["cooldown_active"] else 0,
            1 if snapshot["manual_wake_allowed"] else 0,
            snapshot["thread_ref_hash"],
            1 if snapshot["raw_thread_available"] else 0,
            1 if snapshot["raw_thread_redacted"] else 0,
            json.dumps(snapshot["blocked_reasons"], ensure_ascii=False, sort_keys=True),
            snapshot["ttl_sec"],
            snapshot["schema_hash"],
        ),
    )


def insert_thread_ref(conn: sqlite3.Connection, tick_id: int, now: str, snapshot: Dict[str, Any]) -> None:
    if not snapshot["thread_ref_hash"]:
        return
    conn.execute(
        """
        INSERT INTO wake_thread_refs(tick_id, created_at, thread_ref_hash, raw_thread_available, raw_thread_redacted, ttl_sec)
        VALUES(?,?,?,?,?,?)
        """,
        (
            tick_id,
            now,
            snapshot["thread_ref_hash"],
            1 if snapshot["raw_thread_available"] else 0,
            1 if snapshot["raw_thread_redacted"] else 0,
            snapshot["ttl_sec"],
        ),
    )


def insert_recommendation(
    conn: sqlite3.Connection,
    tick_id: int,
    now: str,
    recommendation: Dict[str, Any],
) -> None:
    conn.execute(
        """
        INSERT INTO wake_guardian_recommendations(tick_id, created_at, recommendation, confidence, execute_allowed, reason)
        VALUES(?,?,?,?,?,?)
        """,
        (
            tick_id,
            now,
            recommendation["recommendation"],
            recommendation["confidence"],
            1 if recommendation["execute_allowed"] else 0,
            recommendation["reason"],
        ),
    )


def insert_closure(conn: sqlite3.Connection, tick_id: int, now: str, closure: Dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO wake_closures(tick_id, created_at, closure_state, next_tick_after_sec, safe_to_sleep, reason)
        VALUES(?,?,?,?,?,?)
        """,
        (
            tick_id,
            now,
            closure["closure_state"],
            closure["next_tick_after_sec"],
            1 if closure["safe_to_sleep"] else 0,
            closure["reason"],
        ),
    )


def insert_audit(conn: sqlite3.Connection, tick_id: int, now: str, event: str, details: Dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO wake_audit(tick_id, created_at, event, details_json) VALUES(?,?,?,?)",
        (tick_id, now, event, json.dumps(details, ensure_ascii=False, sort_keys=True)),
    )


def tick(state_dir: Path, snapshot_path: Path, mode: str) -> Dict[str, Any]:
    db = init_state(state_dir)
    raw_snapshot = load_snapshot(snapshot_path)
    snapshot = normalize_snapshot(raw_snapshot)
    assessment, packet = evaluate_snapshot(snapshot, mode)
    closure = closure_for(assessment["activation"], assessment["reason"])
    recommendation = recommendation_for(assessment, snapshot)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    conn = sqlite3.connect(db)
    try:
        cursor = conn.execute(
            """
            INSERT INTO wake_ticks(created_at, mode, activation, confidence, guardian_action, reason, thread_sync_needed, snapshot_hash)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                now,
                mode,
                assessment["activation"],
                assessment["confidence"],
                assessment["guardian_action"],
                assessment["reason"],
                1 if assessment["thread_sync_needed"] else 0,
                stable_hash(snapshot),
            ),
        )
        tick_id = cursor.lastrowid
        insert_snapshot(conn, tick_id, now, snapshot)
        insert_thread_ref(conn, tick_id, now, snapshot)
        insert_recommendation(conn, tick_id, now, recommendation)
        insert_closure(conn, tick_id, now, closure)
        insert_audit(conn, tick_id, now, "tick_evaluated", {
            "activation": assessment["activation"],
            "mode": mode,
            "blocked_reasons": snapshot["blocked_reasons"],
            "closure_state": closure["closure_state"],
        })
        if packet is not None:
            conn.execute(
                "INSERT INTO thread_sync_packets(tick_id, created_at, packet_json) VALUES(?,?,?)",
                (tick_id, now, json.dumps(packet, ensure_ascii=False, sort_keys=True)),
            )
        conn.commit()
    finally:
        conn.close()
    assessment["tick_id"] = tick_id
    assessment["thread_sync_packet"] = packet
    assessment["closure"] = closure
    assessment["guardian_recommendation"] = recommendation
    assessment["snapshot_hash"] = stable_hash(snapshot)
    return assessment


def summary(state_dir: Path) -> Dict[str, Any]:
    db = init_state(state_dir)
    conn = sqlite3.connect(db)
    try:
        total = conn.execute("SELECT COUNT(*) FROM wake_ticks").fetchone()[0]
        rows = conn.execute(
            "SELECT activation, COUNT(*) FROM wake_ticks GROUP BY activation ORDER BY COUNT(*) DESC"
        ).fetchall()
        latest = conn.execute(
            "SELECT activation, confidence, guardian_action, reason FROM wake_ticks ORDER BY tick_id DESC LIMIT 1"
        ).fetchone()
        closures = conn.execute(
            "SELECT closure_state, COUNT(*) FROM wake_closures GROUP BY closure_state ORDER BY COUNT(*) DESC"
        ).fetchall()
        recommendations = conn.execute(
            "SELECT recommendation, COUNT(*) FROM wake_guardian_recommendations GROUP BY recommendation ORDER BY COUNT(*) DESC"
        ).fetchall()
        schema_versions = conn.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()
    finally:
        conn.close()
    return {
        "total_ticks": total,
        "activations": dict(rows),
        "closures": dict(closures),
        "guardian_recommendations": dict(recommendations),
        "schema_versions": [row[0] for row in schema_versions],
        "latest": {
            "activation": latest[0],
            "confidence": latest[1],
            "guardian_action": latest[2],
            "reason": latest[3],
        } if latest else None,
        "safe_action": "observe-only; no LLM/network/publish action",
    }


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Observe-only Airin wakefulness node")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--state-dir", required=True)

    p_tick = sub.add_parser("tick")
    p_tick.add_argument("--state-dir", required=True)
    p_tick.add_argument("--snapshot", required=True)
    p_tick.add_argument("--mode", choices=sorted(ALLOWED_MODES), default="observe")

    p_summary = sub.add_parser("summary")
    p_summary.add_argument("--state-dir", required=True)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "init":
            print_json({"db": str(init_state(Path(args.state_dir))), "status": "ok"})
        elif args.cmd == "tick":
            print_json(tick(Path(args.state_dir), Path(args.snapshot), args.mode))
        elif args.cmd == "summary":
            print_json(summary(Path(args.state_dir)))
        return 0
    except Exception as exc:
        print_json({"status": "error", "error": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
