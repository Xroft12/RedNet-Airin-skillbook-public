from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def hermes_root() -> Path:
    base = os.getenv("LOCALAPPDATA")
    if base:
        return Path(base) / "hermes"
    return Path.home() / ".hermes"


ROOT = hermes_root()
SCRIPT_PATH = ROOT / "scripts" / "airin_neural_service_node.py"
MODULE_STATUS_SCRIPT = ROOT / "scripts" / "airin_module_status.py"
STATE_DIR = ROOT / "state" / "neural-service-node"
DB_PATH = STATE_DIR / "airin-neural-service-node.sqlite3"
CONFIG_PATH = STATE_DIR / "config.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def default_config() -> dict[str, Any]:
    return {
        "service": "airin-neural-service-node",
        "stage": 1,
        "enabled": True,
        "mode": "observe",
        "agent_id": "airin",
        "lmstudio_base_url": "http://127.0.0.1:1234/v1",
        "model": "qwen2.5-coder-1.5b-instruct",
        "timeout_seconds": 60,
        "max_input_chars": 12000,
        "strict_json": True,
        "allow_actions": False,
        "forbidden_actions": [
            "repair_desktop",
            "retry_desktop",
            "update_desktop",
            "reset_gateway",
            "stop_gateway",
            "change_default_route",
            "change_vpn",
            "change_tailscale",
            "change_ssh",
            "change_edgerouter",
        ],
        "created_at": now_iso(),
    }


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    ensure_dirs()
    if not CONFIG_PATH.exists():
        cfg = default_config()
        save_config(cfg)
        return cfg
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("config must be object")
    except Exception:
        data = default_config()
        data["mode"] = "observe"
        data["recovered_at"] = now_iso()
        save_config(data)
    base = default_config()
    base.update(data)
    base["timeout_seconds"] = max(30, int(base.get("timeout_seconds") or 60))
    return base


def save_config(cfg: dict[str, Any]) -> None:
    ensure_dirs()
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def connect_db() -> sqlite3.Connection:
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("pragma journal_mode=wal")
    conn.execute(
        """
        create table if not exists assessments(
            id text primary key,
            created_at text not null,
            agent_id text not null,
            source text not null,
            mode text not null,
            model text not null,
            used_llm integer not null,
            state text not null,
            severity text not null,
            confidence real not null,
            recommendation text not null,
            input_json text not null,
            result_json text not null,
            raw_response text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists service_state(
            key text primary key,
            value text not null,
            updated_at text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists node_events(
            id text primary key,
            created_at text not null,
            source text not null,
            event_json text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists node_assessments(
            id text primary key,
            event_id text,
            created_at text not null,
            node_id text not null,
            source text not null,
            mode text not null,
            state text not null,
            severity text not null,
            confidence real not null,
            used_llm integer not null,
            assessment_json text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists node_recommendations(
            id text primary key,
            assessment_id text,
            created_at text not null,
            source text not null,
            mode text not null,
            recommendation text not null,
            status text not null,
            action_allowed integer not null,
            reason text not null,
            result_json text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists node_feedback(
            id text primary key,
            recommendation_id text,
            created_at text not null,
            outcome text not null,
            notes text not null,
            feedback_json text not null
        )
        """
    )
    conn.execute(
        """
        create table if not exists attempt_patterns(
            id text primary key,
            created_at text not null,
            updated_at text not null,
            pattern_key text not null unique,
            state text not null,
            recommendation text not null,
            success_count integer not null default 0,
            failure_count integer not null default 0,
            harm_count integer not null default 0,
            ttl_seconds integer not null default 604800,
            usefulness real not null default 0.0,
            risk real not null default 0.0,
            pattern_json text not null
        )
        """
    )
    conn.commit()
    return conn


def run_json(args: list[str], timeout: int = 30) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        proc = subprocess.run(
            args,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=env,
        )
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}
    text = (proc.stdout or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        if proc.returncode != 0:
            return dict(ok=False, returncode=proc.returncode, stdout=text[-2000:], stderr=(proc.stderr or "")[-2000:])
        return dict(ok=False, error="json_decode_failed", text=text[-2000:])
    if not isinstance(data, dict):
        return {"ok": False, "error": "json_not_object"}
    data.setdefault("ok", proc.returncode == 0)
    if proc.returncode != 0:
        data.setdefault("returncode", proc.returncode)
        data.setdefault("stderr", (proc.stderr or "")[-2000:])
    return data


def collect_module_status() -> dict[str, Any]:
    if not MODULE_STATUS_SCRIPT.exists():
        return {"ok": False, "error": "module_status_missing", "path": str(MODULE_STATUS_SCRIPT)}
    return run_json([sys.executable, str(MODULE_STATUS_SCRIPT)], timeout=45)


def compact_status(snapshot: dict[str, Any]) -> dict[str, Any]:
    launch = snapshot.get("hermes_launch_survival") if isinstance(snapshot.get("hermes_launch_survival"), dict) else {}
    launch_counts = launch.get("process_counts") if isinstance(launch.get("process_counts"), dict) else {}
    queue = snapshot.get("subagent_queue") if isinstance(snapshot.get("subagent_queue"), dict) else {}
    guardian = snapshot.get("guardian") if isinstance(snapshot.get("guardian"), dict) else {}
    guardian_state = guardian.get("guardian") if isinstance(guardian.get("guardian"), dict) else {}
    local_chat = snapshot.get("local_chat") if isinstance(snapshot.get("local_chat"), dict) else {}
    diary = snapshot.get("diary") if isinstance(snapshot.get("diary"), dict) else {}
    signal_sensor = snapshot.get("signal_sensor") if isinstance(snapshot.get("signal_sensor"), dict) else {}
    sensor_latest = signal_sensor.get("latest") if isinstance(signal_sensor.get("latest"), dict) else {}
    sensor_tables = signal_sensor.get("tables") if isinstance(signal_sensor.get("tables"), dict) else {}
    sensor_classifier = signal_sensor.get("classifier") if isinstance(signal_sensor.get("classifier"), dict) else {}
    return {
        "ok": bool(snapshot.get("ok")),
        "warnings": snapshot.get("warnings") if isinstance(snapshot.get("warnings"), list) else [],
        "skills": (snapshot.get("presence") or {}).get("skills", {}) if isinstance(snapshot.get("presence"), dict) else {},
        "guardian": {
            "mode": guardian_state.get("mode"),
            "held_requests": guardian_state.get("held_requests"),
            "queue_depth": guardian_state.get("queue_depth"),
            "recommended_action": guardian_state.get("recommended_action"),
        },
        "subagent_queue": {
            "active_count": queue.get("active_count"),
            "dlq_count": queue.get("dlq_count"),
            "max_size": queue.get("max_size"),
            "core_only": queue.get("core_only"),
        },
        "diary": {
            "signals": diary.get("signals"),
            "capsules": diary.get("capsules"),
            "textual_crons_by_state": diary.get("textual_crons_by_state"),
        },
        "launch_survival": {
            "mode": launch.get("mode"),
            "task_installed": launch.get("task_installed"),
            "gateway_count": launch_counts.get("gateway", 0),
            "desktop_count": launch_counts.get("packaged_desktop", 0),
            "control_center_count": launch_counts.get("control_center", 0),
            "local_chat_count": launch_counts.get("local_chat", 0),
            "desktop_symptoms": (launch.get("desktop_log") or {}).get("symptoms", []) if isinstance(launch.get("desktop_log"), dict) else [],
        },
        "local_chat": {
            "ok": local_chat.get("ok"),
            "enabled": local_chat.get("enabled"),
            "messages": local_chat.get("messages"),
            "queue": local_chat.get("queue"),
        },
        "signal_sensor": {
            "ok": signal_sensor.get("ok"),
            "mode": signal_sensor.get("mode"),
            "allow_actions": signal_sensor.get("allow_actions"),
            "events": sensor_tables.get("sensor_events"),
            "labels": sensor_classifier.get("labels"),
            "weights": sensor_classifier.get("weights"),
            "latest_state": sensor_latest.get("state"),
            "latest_severity": sensor_latest.get("severity"),
            "latest_confidence": sensor_latest.get("confidence"),
            "latest_recommendation": sensor_latest.get("recommendation"),
        },
    }


def heuristic_assessment(compact: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    launch = compact.get("launch_survival") if isinstance(compact.get("launch_survival"), dict) else {}
    warnings = compact.get("warnings") if isinstance(compact.get("warnings"), list) else []
    evidence: list[str] = []
    state = "stable"
    severity = "normal"
    recommendation = "observe"
    confidence = 0.62

    if launch.get("gateway_count") == 1:
        evidence.append("gateway_alive")
    else:
        state = "gateway_ambiguous"
        severity = "critical"
        recommendation = "human_check_gateway_before_any_restart"
        confidence = 0.76

    if int(launch.get("desktop_count", 0) or 0) > 0:
        evidence.append("packaged_desktop_present")
        state = "desktop_loop_risk"
        severity = "warning"
        recommendation = "keep_launch_survival_hold"
        confidence = max(confidence, 0.78)
    else:
        evidence.append("packaged_desktop_absent")

    if launch.get("mode") == "hold":
        evidence.append("launch_survival_hold")
    if launch.get("task_installed"):
        evidence.append("launch_survival_task_installed")
    if warnings:
        evidence.append("module_warnings_present")
        severity = "warning" if severity == "normal" else severity

    if state == "stable":
        recommendation = "keep_observing_and_do_not_change_routes"
        confidence = 0.82 if compact.get("ok") else 0.68

    return {
        "state": state,
        "severity": severity,
        "confidence": round(float(confidence), 2),
        "evidence": evidence,
        "recommendation": recommendation,
        "forbidden": list(cfg.get("forbidden_actions") or []),
        "notes": "read-only assessment; no network or gateway action was executed",
    }


def lmstudio_health(cfg: dict[str, Any]) -> dict[str, Any]:
    base_url = str(cfg.get("lmstudio_base_url") or "http://127.0.0.1:1234/v1")
    if not is_loopback_url(base_url):
        return dict(ok=False, error="non_loopback_lmstudio_base_url", detail="Stage 1 permits only localhost/loopback LM Studio endpoints")
    url = base_url.rstrip("/") + "/models"
    try:
        with urllib.request.urlopen(url, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as exc:
        return dict(ok=False, error=type(exc).__name__, detail=str(exc))
    models = [item.get("id") for item in data.get("data", []) if isinstance(item, dict)]
    return dict(ok=True, models=models, selected=cfg.get("model"), selected_available=cfg.get("model") in models)


def call_lmstudio(compact: dict[str, Any], cfg: dict[str, Any]) -> tuple[bool, dict[str, Any], str]:
    base_url = str(cfg.get("lmstudio_base_url") or "http://127.0.0.1:1234/v1")
    if not is_loopback_url(base_url):
        return False, dict(error="non_loopback_lmstudio_base_url", detail="Stage 1 permits only localhost/loopback LM Studio endpoints"), ""
    base = base_url.rstrip("/")
    url = base + "/chat/completions"
    model = str(cfg.get("model") or "qwen2.5-coder-1.5b-instruct")
    payload_text = json.dumps(compact, ensure_ascii=False)
    max_chars = int(cfg.get("max_input_chars") or 12000)
    if len(payload_text) > max_chars:
        payload_text = payload_text[:max_chars] + "...TRUNCATED"
    system = (
        "Ты сервисный нейро-сигнализатор Айрин. "
        "Ты не управляешь сетью, не запускаешь команды и не предлагаешь опасные действия. "
        "Верни только JSON с ключами state, severity, confidence, evidence, recommendation, forbidden, notes. "
        "severity: normal|warning|critical. confidence от 0 до 1."
    )
    body = dict(
        model=model,
        messages=[
            dict(role="system", content=system),
            dict(role="user", content="Оцени этот статус Айрин:\n" + payload_text),
        ],
        temperature=0.1,
        max_tokens=500,
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=int(cfg.get("timeout_seconds") or 24)) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return False, {"error": type(exc).__name__, "detail": str(exc)}, ""
    try:
        data = json.loads(raw)
        text = data["choices"][0]["message"]["content"]
    except Exception as exc:
        return False, {"error": "bad_lmstudio_response", "detail": str(exc)}, raw[-2000:]
    cleaned = str(text).strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        return False, dict(error="model_json_decode_failed", text=cleaned[-2000:]), raw[-2000:]
    if not isinstance(result, dict):
        return False, {"error": "model_json_not_object"}, raw[-2000:]
    return True, result, raw[-4000:]


SECRET_LIKE_PATTERNS = [
    re.compile(r"(?i)\bauthorization\s*[:=]"),
    re.compile(r"(?i)\bbearer\s+\S+"),
    re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key)\s*[:=]"),
    re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY)[A-Z0-9_]*\s*[:=]"),
    re.compile(r"\bsk-[A-Za-z0-9_.-]{8,}\b"),
]



def is_loopback_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(value)
    except Exception:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").strip().lower()
    return host in {"localhost", "127.0.0.1", "::1"}

def redact_evidence_item(value: Any) -> str:
    text = str(value)
    for pattern in SECRET_LIKE_PATTERNS:
        if pattern.search(text):
            return "[redacted-secret-like-evidence]"
    return text



def redact_secret_like_data(value: Any) -> Any:
    if isinstance(value, dict):
        safe: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if redact_evidence_item(key_text) != key_text:
                safe[key_text] = "[redacted-secret-like-value]"
            else:
                safe[key_text] = redact_secret_like_data(item)
        return safe
    if isinstance(value, list):
        return [redact_secret_like_data(item) for item in value]
    if isinstance(value, tuple):
        return [redact_secret_like_data(item) for item in value]
    if isinstance(value, str):
        return redact_evidence_item(value)
    return value

def normalize_assessment(result: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    severity = str(result.get("severity") or "warning")
    if severity not in {"normal", "warning", "critical"}:
        severity = "warning"
    try:
        confidence = float(result.get("confidence", 0.5))
    except Exception:
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))
    evidence = result.get("evidence") if isinstance(result.get("evidence"), list) else []
    forbidden = result.get("forbidden") if isinstance(result.get("forbidden"), list) else []
    merged_forbidden = sorted(set(str(x) for x in forbidden + list(cfg.get("forbidden_actions") or [])))
    normalized = {
        "state": str(result.get("state") or "unknown"),
        "severity": severity,
        "confidence": round(confidence, 2),
        "evidence": [redact_evidence_item(x) for x in evidence][:12],
        "recommendation": str(result.get("recommendation") or "observe"),
        "forbidden": merged_forbidden,
        "notes": str(result.get("notes") or "read-only assessment"),
    }
    if "llm_error" in result:
        normalized["llm_error"] = result["llm_error"]
    return normalized


def store_assessment(source: str, compact: dict[str, Any], result: dict[str, Any], raw: str, used_llm: bool, cfg: dict[str, Any]) -> str:
    assessment_id = uuid.uuid4().hex
    event_id = uuid.uuid4().hex
    created = now_iso()
    mode = str(cfg.get("mode") or "observe")
    safe_compact = redact_secret_like_data(compact)
    safe_result = redact_secret_like_data(result)
    result_json = json.dumps(safe_result, ensure_ascii=False)
    input_json = json.dumps(safe_compact, ensure_ascii=False)
    raw_response = redact_evidence_item(raw[-4000:])
    with closing(connect_db()) as conn:
        conn.execute(
            "insert into node_events(id, created_at, source, event_json) values(?,?,?,?)",
            (event_id, created, source, input_json),
        )
        conn.execute(
            """
            insert into assessments(id, created_at, agent_id, source, mode, model, used_llm, state, severity,
                                    confidence, recommendation, input_json, result_json, raw_response)
            values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                assessment_id,
                created,
                str(cfg.get("agent_id") or "airin"),
                source,
                mode,
                str(cfg.get("model") or ""),
                1 if used_llm else 0,
                str(result.get("state") or "unknown"),
                str(result.get("severity") or "warning"),
                float(result.get("confidence") or 0.0),
                str(result.get("recommendation") or "observe"),
                input_json,
                result_json,
                raw_response,
            ),
        )
        conn.execute(
            """
            insert into node_assessments(id, event_id, created_at, node_id, source, mode, state, severity,
                                         confidence, used_llm, assessment_json)
            values(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                assessment_id,
                event_id,
                created,
                "airin-neural-service-node",
                source,
                mode,
                str(result.get("state") or "unknown"),
                str(result.get("severity") or "warning"),
                float(result.get("confidence") or 0.0),
                1 if used_llm else 0,
                result_json,
            ),
        )
        conn.execute(
            "insert or replace into service_state(key, value, updated_at) values(?,?,?)",
            ("latest_assessment", result_json, created),
        )
        conn.commit()
    return assessment_id


def record_recommendation(assessment_id: str, source: str, result: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any] | None:
    mode = str(cfg.get("mode") or "observe")
    if mode not in {"advise", "hold", "act"}:
        return None
    recommendation = str(result.get("recommendation") or "observe")
    action_allowed = False
    status_value = "pending" if mode in {"advise", "hold"} else "blocked"
    advice_id = uuid.uuid4().hex
    advice = {
        "id": advice_id,
        "assessment_id": assessment_id,
        "mode": mode,
        "recommendation": recommendation,
        "status": status_value,
        "action_allowed": action_allowed,
        "reason": "stage1_advise_only_no_action_execution",
    }
    created = now_iso()
    with closing(connect_db()) as conn:
        conn.execute(
            """
            insert into node_recommendations(id, assessment_id, created_at, source, mode, recommendation,
                                             status, action_allowed, reason, result_json)
            values(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                advice_id,
                assessment_id,
                created,
                source,
                mode,
                recommendation,
                status_value,
                1 if action_allowed else 0,
                str(advice.get("reason") or ""),
                json.dumps(redact_secret_like_data(result), ensure_ascii=False),
            ),
        )
        conn.execute(
            "insert or replace into service_state(key, value, updated_at) values(?,?,?)",
            ("latest_recommendation", json.dumps(advice, ensure_ascii=False), created),
        )
        conn.commit()
    return advice


def assess(args: argparse.Namespace) -> dict[str, Any]:
    cfg = load_config()
    force_mode = getattr(args, "force_mode", None)
    if force_mode:
        cfg = dict(cfg)
        cfg["mode"] = str(force_mode)
        cfg["allow_actions"] = False
    snapshot = collect_module_status()
    compact = redact_secret_like_data(compact_status(snapshot))
    used_llm = False
    raw = ""
    if cfg.get("enabled") and str(cfg.get("mode") or "observe") != "off":
        ok, model_result, raw = call_lmstudio(compact, cfg)
        if ok:
            result = normalize_assessment(model_result, cfg)
            used_llm = True
        else:
            fallback = heuristic_assessment(compact, cfg)
            fallback["llm_error"] = model_result
            result = normalize_assessment(fallback, cfg)
    else:
        result = normalize_assessment(heuristic_assessment(compact, cfg), cfg)
    assessment_id = store_assessment(str(args.source), compact, result, raw, used_llm, cfg)
    advice = record_recommendation(assessment_id, str(args.source), result, cfg)
    response = {
        "ok": True,
        "service": "airin-neural-service-node",
        "stage": cfg.get("stage", 1),
        "mode": cfg.get("mode"),
        "used_llm": used_llm,
        "model": cfg.get("model"),
        "assessment": result,
        "db": str(DB_PATH),
    }
    if advice:
        response["advice"] = advice
    return response


def status() -> dict[str, Any]:
    cfg = load_config()
    with closing(connect_db()) as conn:
        total = conn.execute("select count(*) from assessments").fetchone()[0]
        latest_row = conn.execute(
            "select created_at, state, severity, confidence, recommendation, used_llm from assessments order by created_at desc limit 1"
        ).fetchone()
    latest = None
    if latest_row:
        latest = {
            "created_at": latest_row[0],
            "state": latest_row[1],
            "severity": latest_row[2],
            "confidence": latest_row[3],
            "recommendation": latest_row[4],
            "used_llm": bool(latest_row[5]),
        }
    lmstudio = lmstudio_health(cfg)
    llm_ready = bool(lmstudio.get("ok") and lmstudio.get("selected_available"))
    return {
        "ok": True,
        "service": "airin-neural-service-node",
        "mode": cfg.get("mode"),
        "enabled": bool(cfg.get("enabled")),
        "allow_actions": bool(cfg.get("allow_actions")),
        "model": cfg.get("model"),
        "llm_ready": llm_ready,
        "lmstudio": lmstudio,
        "assessments": total,
        "latest": latest,
        "db": str(DB_PATH),
        "config": str(CONFIG_PATH),
    }


def set_mode(mode: str, reason: str) -> dict[str, Any]:
    if mode not in {"off", "observe", "advise", "hold", "act"}:
        return {"ok": False, "error": "bad_mode", "allowed": ["off", "observe", "advise", "hold", "act"]}
    cfg = load_config()
    if mode == "act":
        cfg["allow_actions"] = False
        reason = (reason + "; act requested but actions remain disabled").strip()
    cfg["mode"] = mode
    cfg["updated_at"] = now_iso()
    cfg["reason"] = reason
    save_config(cfg)
    return {"ok": True, "mode": mode, "allow_actions": cfg.get("allow_actions"), "reason": reason}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Read-only neural service node for Airin.")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("init")
    sub.add_parser("status")
    assess_parser = sub.add_parser("assess")
    assess_parser.add_argument("--source", default="module-status")
    assess_parser.set_defaults(force_mode=None)
    advise_parser = sub.add_parser("advise")
    advise_parser.add_argument("--source", default="manual-advise")
    advise_parser.set_defaults(force_mode="advise")
    mode_parser = sub.add_parser("set-mode")
    mode_parser.add_argument("mode")
    mode_parser.add_argument("--reason", default="")
    args = parser.parse_args()

    if args.cmd == "init":
        load_config()
        connect_db().close()
        result = status()
    elif args.cmd == "status" or not args.cmd:
        result = status()
    elif args.cmd in {"assess", "advise"}:
        result = assess(args)
    elif args.cmd == "set-mode":
        result = set_mode(args.mode, args.reason)
    else:
        result = {"ok": False, "error": "unknown_command"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
