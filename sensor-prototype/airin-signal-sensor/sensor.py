#!/usr/bin/env python3
"""Observe-only replay sensor for REDNET Airin Skillbook.

The sensor consumes JSONL flow-like events, stores safe metadata in SQLite,
and creates Guardian recommendations without changing routes, firewall, VPN,
or live services.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple


SAFE_SALT = "rednet-airin-signal-sensor-v1"
ALLOWED_LABELS = {"ok", "degraded", "suspicious", "unknown", "noise"}
COMMON_PORTS = {22, 53, 80, 123, 443, 853, 8443, 8080}


SCHEMA = """
CREATE TABLE IF NOT EXISTS sensor_events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_time TEXT,
  source TEXT NOT NULL,
  event_type TEXT NOT NULL,
  src_hash TEXT,
  dst_hash TEXT,
  src_port INTEGER,
  dst_port INTEGER,
  proto TEXT,
  direction TEXT,
  raw_ref TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sensor_features (
  feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  flow_key TEXT NOT NULL,
  bytes_in INTEGER DEFAULT 0,
  bytes_out INTEGER DEFAULT 0,
  packets_in INTEGER DEFAULT 0,
  packets_out INTEGER DEFAULT 0,
  duration REAL DEFAULT 0,
  reset_count INTEGER DEFAULT 0,
  dns_rcode TEXT,
  tls_state TEXT,
  http_status INTEGER,
  frequency_bucket TEXT,
  flags TEXT,
  FOREIGN KEY(event_id) REFERENCES sensor_events(event_id)
);

CREATE TABLE IF NOT EXISTS sensor_assessments (
  assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  label TEXT NOT NULL CHECK(label IN ('ok','degraded','suspicious','unknown','noise')),
  confidence REAL NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(event_id) REFERENCES sensor_events(event_id)
);

CREATE TABLE IF NOT EXISTS pattern_memory (
  pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
  pattern_key TEXT NOT NULL UNIQUE,
  label TEXT NOT NULL,
  success_count INTEGER DEFAULT 0,
  fail_count INTEGER DEFAULT 0,
  confidence REAL DEFAULT 0.5,
  expires_at TEXT,
  last_seen TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS guardian_recommendations (
  recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER NOT NULL,
  mode TEXT NOT NULL DEFAULT 'observe',
  recommendation TEXT NOT NULL,
  rationale TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(event_id) REFERENCES sensor_events(event_id)
);
"""


def now_text() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def db_path(state_dir: Path) -> Path:
    return state_dir / "airin_signal_sensor.sqlite3"


def connect(state_dir: Path) -> sqlite3.Connection:
    state_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path(state_dir))
    conn.row_factory = sqlite3.Row
    return conn


def init_state(state_dir: Path) -> Path:
    conn = connect(state_dir)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
    return db_path(state_dir)


def stable_hash(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    digest = hashlib.sha256((SAFE_SALT + ":" + text).encode("utf-8")).hexdigest()
    return digest[:16]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def first_present(event: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in event and event[key] not in (None, ""):
            return event[key]
    return None


def nested(event: Dict[str, Any], section: str, key: str) -> Any:
    value = event.get(section)
    if isinstance(value, dict):
        return value.get(key)
    return None


def sanitize_event(event: Dict[str, Any], source: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    event_type = str(first_present(event, "event_type", "type", "kind") or "flow").lower()
    proto = str(first_present(event, "proto", "protocol") or "tcp").lower()
    src_port = as_int(first_present(event, "src_port", "sport"))
    dst_port = as_int(first_present(event, "dest_port", "dst_port", "dport"))
    src_identity = first_present(event, "src_ip", "src", "source_ip", "source")
    dst_identity = first_present(event, "dest_ip", "dst_ip", "dest", "destination_ip", "destination")
    dns_name = nested(event, "dns", "rrname") or first_present(event, "dns_query", "query")
    if dns_name and not dst_identity:
        dst_identity = dns_name
    event_time = str(first_present(event, "timestamp", "ts", "time") or now_text())

    bytes_out = as_int(first_present(event, "bytes_out", "bytes_toserver", "tx_bytes", "sent_bytes"))
    bytes_in = as_int(first_present(event, "bytes_in", "bytes_toclient", "rx_bytes", "recv_bytes"))
    packets_out = as_int(first_present(event, "packets_out", "pkts_toserver", "tx_packets"))
    packets_in = as_int(first_present(event, "packets_in", "pkts_toclient", "rx_packets"))
    duration = as_float(first_present(event, "duration", "flow_duration"))
    flags = str(first_present(event, "tcp_flags", "flags", "state") or "")
    reset_count = as_int(first_present(event, "reset_count", "tcp_reset_count"))
    if "R" in flags.upper() or "RESET" in flags.upper() or "RST" in flags.upper():
        reset_count = max(reset_count, 1)
    dns_rcode = str(nested(event, "dns", "rcode") or first_present(event, "dns_rcode", "rcode") or "").upper()
    tls_state = str(nested(event, "tls", "state") or first_present(event, "tls_state") or "").lower()
    http_status = as_int(nested(event, "http", "status") or first_present(event, "http_status"))

    safe_event = {
        "event_time": event_time,
        "source": source,
        "event_type": event_type,
        "src_hash": stable_hash(src_identity),
        "dst_hash": stable_hash(dst_identity),
        "src_port": src_port,
        "dst_port": dst_port,
        "proto": proto,
        "direction": str(first_present(event, "direction") or infer_direction(src_port, dst_port)),
    }
    feature = {
        "flow_key": stable_hash(f"{proto}:{src_port}:{dst_port}:{safe_event['src_hash']}:{safe_event['dst_hash']}") or "unknown",
        "bytes_in": bytes_in,
        "bytes_out": bytes_out,
        "packets_in": packets_in,
        "packets_out": packets_out,
        "duration": duration,
        "reset_count": reset_count,
        "dns_rcode": dns_rcode or None,
        "tls_state": tls_state or None,
        "http_status": http_status,
        "frequency_bucket": bucket_frequency(bytes_in + bytes_out, duration),
        "flags": flags[:80],
    }
    safe_event["raw_ref"] = stable_hash(json.dumps(safe_event | feature, sort_keys=True, ensure_ascii=False)) or "empty"
    return safe_event, feature


def infer_direction(src_port: int, dst_port: int) -> str:
    if dst_port in COMMON_PORTS:
        return "outbound"
    if src_port in COMMON_PORTS:
        return "inbound"
    return "unknown"


def bucket_frequency(total_bytes: int, duration: float) -> str:
    if duration <= 0:
        return "instant"
    rate = total_bytes / duration
    if rate < 512:
        return "low"
    if rate < 20000:
        return "medium"
    return "high"


def classify(safe_event: Dict[str, Any], feature: Dict[str, Any], original: Dict[str, Any]) -> Tuple[str, float, str]:
    if "alert" in original or safe_event["event_type"] == "alert":
        return "suspicious", 0.88, "alert event observed; observe-only recommendation"
    dns_rcode = (feature.get("dns_rcode") or "").upper()
    if dns_rcode in {"SERVFAIL", "NXDOMAIN", "TIMEOUT", "REFUSED"}:
        return "degraded", 0.86, f"DNS symptom: {dns_rcode}"
    if feature.get("reset_count", 0) >= 1:
        confidence = 0.82 if feature.get("reset_count", 0) >= 3 else 0.68
        return "degraded", confidence, "TCP reset symptom"
    tls_state = (feature.get("tls_state") or "").lower()
    if tls_state in {"failed", "timeout", "reset"}:
        return "degraded", 0.78, f"TLS symptom: {tls_state}"
    dst_port = safe_event.get("dst_port") or 0
    total_bytes = feature.get("bytes_in", 0) + feature.get("bytes_out", 0)
    if total_bytes <= 64 and feature.get("duration", 0) <= 0.01:
        return "noise", 0.55, "tiny instant event"
    if dst_port and dst_port not in COMMON_PORTS and safe_event.get("event_type") not in {"dns", "flow", "tls", "http"}:
        return "unknown", 0.5, "uncommon port and event type"
    if dst_port in {443, 8443, 53, 853} or safe_event.get("event_type") in {"dns", "tls", "http", "flow"}:
        return "ok", 0.74, "common service metadata without degradation symptoms"
    return "unknown", 0.45, "insufficient signal"


def guardian_recommendation(label: str, reason: str) -> Tuple[str, str, str]:
    if label == "degraded":
        return "observe", "Не менять сеть. Показать деградацию и удержать активные сетевые действия до ручной проверки.", reason
    if label == "suspicious":
        return "observe", "Показать оператору подозрительный сигнал. Не блокировать автоматически.", reason
    if label == "unknown":
        return "observe", "Сохранить как неизвестный паттерн и ждать дополнительных событий.", reason
    if label == "noise":
        return "observe", "Считать шумом до повторяемости. Действий не требуется.", reason
    return "observe", "Состояние выглядит нормально. Действий не требуется.", reason


def insert_event(conn: sqlite3.Connection, event: Dict[str, Any], feature: Dict[str, Any], label: str, confidence: float, reason: str) -> int:
    created_at = now_text()
    cur = conn.execute(
        """
        INSERT INTO sensor_events(event_time, source, event_type, src_hash, dst_hash, src_port, dst_port, proto, direction, raw_ref, created_at)
        VALUES(:event_time, :source, :event_type, :src_hash, :dst_hash, :src_port, :dst_port, :proto, :direction, :raw_ref, :created_at)
        """,
        event | {"created_at": created_at},
    )
    event_id = int(cur.lastrowid)
    conn.execute(
        """
        INSERT INTO sensor_features(event_id, flow_key, bytes_in, bytes_out, packets_in, packets_out, duration, reset_count, dns_rcode, tls_state, http_status, frequency_bucket, flags)
        VALUES(:event_id, :flow_key, :bytes_in, :bytes_out, :packets_in, :packets_out, :duration, :reset_count, :dns_rcode, :tls_state, :http_status, :frequency_bucket, :flags)
        """,
        feature | {"event_id": event_id},
    )
    conn.execute(
        "INSERT INTO sensor_assessments(event_id, label, confidence, reason, created_at) VALUES(?,?,?,?,?)",
        (event_id, label, confidence, reason, created_at),
    )
    mode, recommendation, rationale = guardian_recommendation(label, reason)
    conn.execute(
        "INSERT INTO guardian_recommendations(event_id, mode, recommendation, rationale, created_at) VALUES(?,?,?,?,?)",
        (event_id, mode, recommendation, rationale, created_at),
    )
    update_pattern_memory(conn, event, feature, label, confidence)
    return event_id


def update_pattern_memory(conn: sqlite3.Connection, event: Dict[str, Any], feature: Dict[str, Any], label: str, confidence: float) -> None:
    pattern_key = f"{event.get('event_type')}:{event.get('proto')}:{event.get('dst_port')}:{feature.get('dns_rcode') or '-'}:{label}"
    now = now_text()
    existing = conn.execute("SELECT * FROM pattern_memory WHERE pattern_key=?", (pattern_key,)).fetchone()
    if existing:
        success = int(existing["success_count"]) + (1 if label in {"ok", "noise"} else 0)
        fail = int(existing["fail_count"]) + (1 if label in {"degraded", "suspicious", "unknown"} else 0)
        new_confidence = min(0.99, max(0.05, (float(existing["confidence"]) + confidence) / 2))
        conn.execute(
            "UPDATE pattern_memory SET label=?, success_count=?, fail_count=?, confidence=?, last_seen=? WHERE pattern_key=?",
            (label, success, fail, new_confidence, now, pattern_key),
        )
    else:
        conn.execute(
            """
            INSERT INTO pattern_memory(pattern_key, label, success_count, fail_count, confidence, expires_at, last_seen, notes)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                pattern_key,
                label,
                1 if label in {"ok", "noise"} else 0,
                1 if label in {"degraded", "suspicious", "unknown"} else 0,
                confidence,
                None,
                now,
                "replay-observe",
            ),
        )


def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_no}: expected object")
            yield value


def ingest_replay(state_dir: Path, replay: Path) -> Dict[str, Any]:
    init_state(state_dir)
    counts: Dict[str, int] = {"total": 0, "ok": 0, "degraded": 0, "suspicious": 0, "unknown": 0, "noise": 0}
    conn = connect(state_dir)
    try:
        for original in iter_jsonl(replay):
            safe_event, feature = sanitize_event(original, source=replay.name)
            label, confidence, reason = classify(safe_event, feature, original)
            insert_event(conn, safe_event, feature, label, confidence, reason)
            counts["total"] += 1
            counts[label] += 1
        conn.commit()
    finally:
        conn.close()
    return counts


def status(state_dir: Path) -> Dict[str, Any]:
    init_state(state_dir)
    conn = connect(state_dir)
    try:
        labels = {
            row["label"]: row["count"]
            for row in conn.execute("SELECT label, COUNT(*) AS count FROM sensor_assessments GROUP BY label")
        }
        total = conn.execute("SELECT COUNT(*) AS c FROM sensor_events").fetchone()["c"]
        recommendations = conn.execute("SELECT COUNT(*) AS c FROM guardian_recommendations").fetchone()["c"]
    finally:
        conn.close()
    return {"events": total, "labels": labels, "guardian_recommendations": recommendations, "mode": "observe"}


def assessment_summary(state_dir: Path) -> Dict[str, Any]:
    data = status(state_dir)
    labels = data["labels"]
    if labels.get("suspicious"):
        dominant = "suspicious"
    elif labels.get("degraded"):
        dominant = "degraded"
    elif labels.get("unknown"):
        dominant = "unknown"
    elif labels.get("ok"):
        dominant = "ok"
    else:
        dominant = "empty"
    data["dominant_state"] = dominant
    data["safe_action"] = "observe-only; no network/firewall/VPN action"
    return data


def emit(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Airin observe-only signal sensor")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init")
    init_cmd.add_argument("--state-dir", required=True)

    ingest_cmd = sub.add_parser("ingest")
    ingest_cmd.add_argument("--state-dir", required=True)
    ingest_cmd.add_argument("--replay", required=True)

    status_cmd = sub.add_parser("status")
    status_cmd.add_argument("--state-dir", required=True)

    assess_cmd = sub.add_parser("assess")
    assess_cmd.add_argument("--state-dir", required=True)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    state_dir = Path(args.state_dir)
    if args.command == "init":
        path = init_state(state_dir)
        emit({"ok": True, "mode": "observe", "database": str(path)})
        return 0
    if args.command == "ingest":
        result = ingest_replay(state_dir, Path(args.replay))
        emit({"ok": True, "mode": "observe", "ingested": result})
        return 0
    if args.command == "status":
        emit(status(state_dir))
        return 0
    if args.command == "assess":
        emit(assessment_summary(state_dir))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
