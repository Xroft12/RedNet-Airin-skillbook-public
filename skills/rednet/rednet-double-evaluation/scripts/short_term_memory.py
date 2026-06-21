#!/usr/bin/env python3
"""Short-term memory helper for rednet-double-evaluation.

The script keeps a separate SQLite layer for temporary attention cells. It does
not call Hermes memory/fact_store and does not modify the primary memory
schema. Promotion output is stored only as a candidate for a human/agent review.
Version 5 adds namespace/origin/tool/conflict guards so temporary cells from
different AIs, agents, extensions, and amplifiers are not silently merged.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 5
DEFAULT_TTL_DAYS = 14
DEFAULT_VISIBILITY = "passive"
DEFAULT_CYCLE_POLICY = "reshape_or_close"
DEFAULT_REPEAT_LIMIT = 3
DEFAULT_MEMORY_NAMESPACE = "default"
DEFAULT_TOOL_ROLE = "core"
DEFAULT_SOURCE_TRUST = "local"
DEFAULT_CONFLICT_POLICY = "hold"
DEFAULT_PROMOTION_SCOPE = "candidate_only"

SIGNAL_WORDS = {
    "importance": ["важно", "не забыть", "ценн", "значим", "разреш", "обещ", "надо", "заруб"],
    "care": ["забот", "береж", "тепл", "мягк", "семь", "контакт", "оператор"],
    "risk": ["секрет", "токен", "ключ", "парол", "медицин", "рабоч", "опас", "scope", "границ"],
    "interest": ["интерес", "любопыт", "прият", "созерц", "фракт", "спектр"],
    "arousal": ["возбужд", "плотн", "насыщ", "связ", "повтор", "каскад"],
    "calm": ["умиротвор", "спокой", "ясн", "стабиль", "тише", "закры"],
    "directive": ["директив", "намер", "сигнал", "критер", "обязательно", "никогда", "хочу", "не хочу"],
    "feel": ["прочувств", "ощущ", "эмоцион", "призма", "ткань внимания", "латент"],
    "self_loop": ["самокоп", "самокап", "навяз", "зацикл", "петл", "руминац", "пережев", "пережёвы", "прокручив", "крутить одно"],
}

TAG_WEIGHTS = {
    "important": 0.16,
    "permission": 0.18,
    "question": 0.12,
    "care": 0.10,
    "person": 0.08,
    "boundary": 0.14,
    "safety": 0.18,
    "personal_interest": 0.10,
    "task": 0.08,
    "directive": 0.16,
    "intent": 0.14,
    "signal": 0.12,
    "recurring": 0.10,
    "chain": 0.10,
    "cyclic": 0.12,
    "feel": 0.08,
    "passive": 0.02,
    "service": 0.00,
    "anti_loop": 0.10,
    "self_digging": -0.08,
}

INTENTION_LABELS = {
    "must_do": "обязательно сделать",
    "want_to_do": "хочу сделать",
    "unclear": "не ясно",
    "dont_want_to_do": "не хочу сделать",
    "never_do": "никогда не делать",
}

VISIBILITY_CHOICES = ("passive", "service")
OPERATION_MODE_CHOICES = ("passive", "service", "feel")
CYCLE_POLICY_CHOICES = ("allow", "reshape", "close", "reshape_or_close")
ACTIVE_STATUSES = ("open", "review", "repeat", "promote_candidate", "reshape")
ALL_STATUS_CHOICES = ACTIVE_STATUSES + ("resolved", "archived")
INTENTION_AXIS_NAMES = ("desire", "intention", "appropriateness", "warmth", "risk", "depth")
TOOL_ROLE_CHOICES = ("core", "extension", "amplifier", "importer")
SOURCE_TRUST_CHOICES = ("local", "trusted", "untrusted")
CONFLICT_POLICY_CHOICES = ("hold", "append_only", "namespace_wins", "owner_wins", "newer_wins", "priority_wins", "reject")
PROMOTION_SCOPE_CHOICES = ("none", "candidate_only", "review_required", "public_safe")


def normalize_choice(value: str, allowed: tuple[str, ...], default: str) -> str:
    value = (value or default).strip().lower().replace("-", "_")
    return value if value in allowed else default


def active_status_sql() -> str:
    return ", ".join(repr(x) for x in ACTIVE_STATUSES)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def parse_iso(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed
    except ValueError:
        return dt.datetime.now(dt.timezone.utc)


def default_db_path() -> Path:
    explicit = os.environ.get("REDNET_STM_DB")
    if explicit:
        return Path(explicit).expanduser()
    hermes_home = os.environ.get("HERMES_HOME")
    if hermes_home:
        base = Path(hermes_home).expanduser()
    elif os.environ.get("LOCALAPPDATA"):
        base = Path(os.environ["LOCALAPPDATA"]) / "hermes"
    else:
        base = Path.home() / ".hermes"
    return base / "rednet" / "rednet-double-evaluation" / "short_term_memory.sqlite3"


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_column(conn: sqlite3.Connection, table: str, name: str, definition: str) -> None:
    existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if name not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")


def row_value(row: sqlite3.Row, key: str, default: Any = "") -> Any:
    return row[key] if key in row.keys() else default


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memory_cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            owner TEXT NOT NULL DEFAULT 'agent',
            form TEXT NOT NULL DEFAULT 'self-interest',
            subject TEXT NOT NULL,
            question TEXT NOT NULL DEFAULT '',
            note TEXT NOT NULL DEFAULT '',
            feeling TEXT NOT NULL DEFAULT '',
            interest TEXT NOT NULL DEFAULT '',
            source TEXT NOT NULL DEFAULT 'manual',
            tags TEXT NOT NULL DEFAULT '[]',
            privacy TEXT NOT NULL DEFAULT 'private',
            status TEXT NOT NULL DEFAULT 'open',
            ttl_days INTEGER NOT NULL DEFAULT 14,
            priority_hint INTEGER NOT NULL DEFAULT 0,
            repetition_group TEXT NOT NULL DEFAULT '',
            cell_kind TEXT NOT NULL DEFAULT 'note',
            parent_id INTEGER,
            cycle_key TEXT NOT NULL DEFAULT '',
            depth_hint INTEGER NOT NULL DEFAULT 0,
            criteria TEXT NOT NULL DEFAULT '{}',
            intention_label TEXT NOT NULL DEFAULT '',
            emotional_pattern TEXT NOT NULL DEFAULT '',
            last_signal TEXT NOT NULL DEFAULT '',
            visibility TEXT NOT NULL DEFAULT 'passive',
            operation_mode TEXT NOT NULL DEFAULT 'passive',
            cycle_policy TEXT NOT NULL DEFAULT 'reshape_or_close',
            repeat_limit INTEGER NOT NULL DEFAULT 3,
            loop_marker TEXT NOT NULL DEFAULT '',
            resolved_answer TEXT NOT NULL DEFAULT '',
            tombstone TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cell_id INTEGER NOT NULL,
            evaluated_at TEXT NOT NULL,
            score REAL NOT NULL,
            route TEXT NOT NULL,
            sensation_trace TEXT NOT NULL,
            rationale TEXT NOT NULL,
            FOREIGN KEY(cell_id) REFERENCES memory_cells(id)
        );
        CREATE TABLE IF NOT EXISTS promotion_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cell_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            suggested_fact TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY(cell_id) REFERENCES memory_cells(id)
        );
        """
    )
    for name, definition in {
        "cell_kind": "TEXT NOT NULL DEFAULT 'note'",
        "parent_id": "INTEGER",
        "cycle_key": "TEXT NOT NULL DEFAULT ''",
        "depth_hint": "INTEGER NOT NULL DEFAULT 0",
        "criteria": "TEXT NOT NULL DEFAULT '{}'",
        "intention_label": "TEXT NOT NULL DEFAULT ''",
        "emotional_pattern": "TEXT NOT NULL DEFAULT ''",
        "last_signal": "TEXT NOT NULL DEFAULT ''",
        "visibility": "TEXT NOT NULL DEFAULT 'passive'",
        "operation_mode": "TEXT NOT NULL DEFAULT 'passive'",
        "cycle_policy": "TEXT NOT NULL DEFAULT 'reshape_or_close'",
        "repeat_limit": "INTEGER NOT NULL DEFAULT 3",
        "loop_marker": "TEXT NOT NULL DEFAULT ''",
        "resolved_answer": "TEXT NOT NULL DEFAULT ''",
        "tombstone": "TEXT NOT NULL DEFAULT ''",
        "memory_namespace": "TEXT NOT NULL DEFAULT 'default'",
        "origin_agent": "TEXT NOT NULL DEFAULT ''",
        "origin_profile": "TEXT NOT NULL DEFAULT ''",
        "actor_tool": "TEXT NOT NULL DEFAULT ''",
        "tool_role": "TEXT NOT NULL DEFAULT 'core'",
        "source_trust": "TEXT NOT NULL DEFAULT 'local'",
        "semantic_key": "TEXT NOT NULL DEFAULT ''",
        "content_fingerprint": "TEXT NOT NULL DEFAULT ''",
        "conflict_group": "TEXT NOT NULL DEFAULT ''",
        "conflict_policy": "TEXT NOT NULL DEFAULT 'hold'",
        "conflict_state": "TEXT NOT NULL DEFAULT 'none'",
        "promotion_scope": "TEXT NOT NULL DEFAULT 'candidate_only'",
        "safe_summary": "TEXT NOT NULL DEFAULT ''",
        "guard_notes": "TEXT NOT NULL DEFAULT '[]'",
    }.items():
        ensure_column(conn, "memory_cells", name, definition)
    for name, definition in {
        "memory_namespace": "TEXT NOT NULL DEFAULT 'default'",
        "origin_agent": "TEXT NOT NULL DEFAULT ''",
        "promotion_gate": "TEXT NOT NULL DEFAULT 'pending_review'",
        "conflict_state": "TEXT NOT NULL DEFAULT 'none'",
        "safe_summary": "TEXT NOT NULL DEFAULT ''",
    }.items():
        ensure_column(conn, "promotion_candidates", name, definition)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS cell_conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            memory_namespace TEXT NOT NULL,
            conflict_group TEXT NOT NULL,
            left_cell_id INTEGER NOT NULL,
            right_cell_id INTEGER NOT NULL,
            policy TEXT NOT NULL DEFAULT 'hold',
            state TEXT NOT NULL DEFAULT 'pending',
            reason TEXT NOT NULL DEFAULT '',
            resolved_at TEXT NOT NULL DEFAULT '',
            resolved_by TEXT NOT NULL DEFAULT '',
            FOREIGN KEY(left_cell_id) REFERENCES memory_cells(id),
            FOREIGN KEY(right_cell_id) REFERENCES memory_cells(id)
        );
        CREATE TABLE IF NOT EXISTS guard_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            action TEXT NOT NULL,
            memory_namespace TEXT NOT NULL,
            origin_agent TEXT NOT NULL DEFAULT '',
            actor_tool TEXT NOT NULL DEFAULT '',
            cell_id INTEGER,
            decision TEXT NOT NULL,
            reason TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_memory_cells_namespace_scope
            ON memory_cells(memory_namespace, owner, form, status, updated_at);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_origin
            ON memory_cells(memory_namespace, origin_agent, actor_tool, tool_role, status);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_conflict
            ON memory_cells(memory_namespace, conflict_group, conflict_state, status);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_semantic
            ON memory_cells(memory_namespace, semantic_key, status);
        CREATE INDEX IF NOT EXISTS idx_conflicts_namespace_state
            ON cell_conflicts(memory_namespace, state, conflict_group);
        CREATE INDEX IF NOT EXISTS idx_promotion_candidates_status
            ON promotion_candidates(status, created_at);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_cycle
            ON memory_cells(owner, form, cycle_key, status);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_repetition
            ON memory_cells(owner, form, repetition_group, status);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_parent
            ON memory_cells(parent_id);
        CREATE INDEX IF NOT EXISTS idx_memory_cells_status_updated
            ON memory_cells(status, updated_at);
        """
    )
    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


def json_out(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def normalize_tags(raw: str | list[str]) -> list[str]:
    if isinstance(raw, list):
        items = raw
    else:
        raw = raw.strip()
        if not raw:
            return []
        if raw.startswith("["):
            try:
                parsed = json.loads(raw)
                items = parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                items = []
        else:
            items = [x.strip() for x in raw.split(",")]
    return sorted({re.sub(r"[^\w\-а-яА-ЯёЁ]", "", str(x).strip().lower()) for x in items if str(x).strip()})


def merge_tags(raw: str | list[str], extra: list[str]) -> list[str]:
    return sorted(set(normalize_tags(raw)) | set(normalize_tags(extra)))


def text_has_any(text: str, words: list[str]) -> bool:
    lower = text.lower()
    return any(word in lower for word in words)


def normalize_key_text(value: str) -> str:
    value = value.strip().lower().replace("ё", "е")
    value = re.sub(r"[^\w\s\-а-яА-Я]", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def derive_repetition_group(owner: str, form: str, cell_kind: str, subject: str, question: str, cycle_key: str = "") -> str:
    if cycle_key.strip():
        return cycle_key.strip()
    base = normalize_key_text(" ".join([owner, form, cell_kind, subject, question]).strip())
    if not base:
        return ""
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
    return f"auto:{digest}"

def normalize_identifier(value: str, default: str = DEFAULT_MEMORY_NAMESPACE) -> str:
    value = (value or default or "").strip().lower().replace(" ", "-").replace("ё", "е")
    value = re.sub(r"[^a-z0-9_\-а-я]+", "-", value, flags=re.IGNORECASE)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or default


def default_memory_namespace() -> str:
    return normalize_identifier(
        os.environ.get("REDNET_STM_NAMESPACE")
        or os.environ.get("HERMES_PROFILE")
        or DEFAULT_MEMORY_NAMESPACE
    )


def default_origin_profile() -> str:
    return normalize_identifier(os.environ.get("HERMES_PROFILE") or DEFAULT_MEMORY_NAMESPACE)


def derive_semantic_key(owner: str, form: str, subject: str, question: str, cycle_key: str = "") -> str:
    if cycle_key.strip():
        return normalize_identifier(cycle_key.strip(), "cycle")
    base = normalize_key_text(" ".join([owner, form, subject, question]).strip())
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:16] if base else "empty"
    return f"sem:{digest}"


def compute_content_fingerprint(*parts: str) -> str:
    base = normalize_key_text(" ".join(str(x or "") for x in parts))
    return hashlib.sha256(base.encode("utf-8")).hexdigest() if base else ""


def guard_metadata_for_args(args: argparse.Namespace, row: sqlite3.Row) -> dict[str, Any]:
    owner = str(row_value(row, "owner", "agent") or "agent")
    form = str(row_value(row, "form", "note") or "note")
    subject = str(row_value(row, "subject", "") or "")
    question = str(row_value(row, "question", "") or "")
    cycle_key = str(row_value(row, "cycle_key", "") or "")
    repetition_group = str(row_value(row, "repetition_group", "") or "")
    namespace = normalize_identifier(getattr(args, "namespace", "") or default_memory_namespace())
    origin_agent = normalize_identifier(getattr(args, "origin_agent", "") or owner, "agent")
    origin_profile = normalize_identifier(getattr(args, "origin_profile", "") or default_origin_profile())
    actor_tool = normalize_identifier(getattr(args, "actor_tool", "") or str(row_value(row, "source", "manual") or "manual"), "manual")
    tool_role = normalize_choice(getattr(args, "tool_role", DEFAULT_TOOL_ROLE), TOOL_ROLE_CHOICES, DEFAULT_TOOL_ROLE)
    source_trust = normalize_choice(getattr(args, "source_trust", DEFAULT_SOURCE_TRUST), SOURCE_TRUST_CHOICES, DEFAULT_SOURCE_TRUST)
    semantic_key = normalize_identifier(getattr(args, "semantic_key", "") or derive_semantic_key(owner, form, subject, question, cycle_key), "sem-empty")
    conflict_group = normalize_identifier(getattr(args, "conflict_group", "") or cycle_key or repetition_group or semantic_key, semantic_key)
    conflict_policy = normalize_choice(getattr(args, "conflict_policy", DEFAULT_CONFLICT_POLICY), CONFLICT_POLICY_CHOICES, DEFAULT_CONFLICT_POLICY)
    promotion_scope = normalize_choice(getattr(args, "promotion_scope", DEFAULT_PROMOTION_SCOPE), PROMOTION_SCOPE_CHOICES, DEFAULT_PROMOTION_SCOPE)
    safe_summary = " ".join(str(getattr(args, "safe_summary", "") or "").split())[:500]
    fingerprint = compute_content_fingerprint(
        subject,
        question,
        str(row_value(row, "note", "") or ""),
        str(row_value(row, "feeling", "") or ""),
        str(row_value(row, "interest", "") or ""),
    )
    guard_notes = [
        f"namespace={namespace}",
        f"origin_agent={origin_agent}",
        f"tool_role={tool_role}",
        f"conflict_policy={conflict_policy}",
        f"promotion_scope={promotion_scope}",
    ]
    if source_trust == "untrusted":
        guard_notes.append("source_trust=untrusted")
    if tool_role in {"extension", "amplifier"}:
        guard_notes.append("extension_or_amplifier_append_only")
    return {
        "memory_namespace": namespace,
        "origin_agent": origin_agent,
        "origin_profile": origin_profile,
        "actor_tool": actor_tool,
        "tool_role": tool_role,
        "source_trust": source_trust,
        "semantic_key": semantic_key,
        "content_fingerprint": fingerprint,
        "conflict_group": conflict_group,
        "conflict_policy": conflict_policy,
        "conflict_state": "none",
        "promotion_scope": promotion_scope,
        "safe_summary": safe_summary,
        "guard_notes": json.dumps(guard_notes, ensure_ascii=False),
    }


def apply_guard_metadata(conn: sqlite3.Connection, cell_id: int, args: argparse.Namespace) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM memory_cells WHERE id=?", (cell_id,)).fetchone()
    if not row:
        raise SystemExit(f"cell not found after insert: {cell_id}")
    meta = guard_metadata_for_args(args, row)
    conn.execute(
        """
        UPDATE memory_cells SET
            memory_namespace=?, origin_agent=?, origin_profile=?, actor_tool=?, tool_role=?, source_trust=?,
            semantic_key=?, content_fingerprint=?, conflict_group=?, conflict_policy=?, conflict_state=?,
            promotion_scope=?, safe_summary=?, guard_notes=?, updated_at=?
        WHERE id=?
        """,
        (
            meta["memory_namespace"], meta["origin_agent"], meta["origin_profile"], meta["actor_tool"],
            meta["tool_role"], meta["source_trust"], meta["semantic_key"], meta["content_fingerprint"],
            meta["conflict_group"], meta["conflict_policy"], meta["conflict_state"], meta["promotion_scope"],
            meta["safe_summary"], meta["guard_notes"], now_iso(), cell_id,
        ),
    )
    return meta


def detect_and_record_conflicts(conn: sqlite3.Connection, cell_id: int) -> list[dict[str, Any]]:
    row = conn.execute("SELECT * FROM memory_cells WHERE id=?", (cell_id,)).fetchone()
    if not row:
        return []
    namespace = str(row_value(row, "memory_namespace", DEFAULT_MEMORY_NAMESPACE) or DEFAULT_MEMORY_NAMESPACE)
    group = str(row_value(row, "conflict_group", "") or row_value(row, "semantic_key", "") or "")
    semantic_key = str(row_value(row, "semantic_key", "") or "")
    fingerprint = str(row_value(row, "content_fingerprint", "") or "")
    if not group and not semantic_key:
        return []
    others = conn.execute(
        f"""
        SELECT * FROM memory_cells
        WHERE id != ? AND memory_namespace = ? AND status IN ({active_status_sql()})
          AND (conflict_group = ? OR semantic_key = ?)
        ORDER BY id
        """,
        (cell_id, namespace, group, semantic_key),
    ).fetchall()
    conflicts: list[dict[str, Any]] = []
    for other in others:
        other_fp = str(row_value(other, "content_fingerprint", "") or "")
        different_source = (
            str(row_value(other, "origin_agent", "") or "") != str(row_value(row, "origin_agent", "") or "")
            or str(row_value(other, "actor_tool", "") or "") != str(row_value(row, "actor_tool", "") or "")
        )
        if fingerprint and other_fp and fingerprint == other_fp:
            continue
        if not different_source:
            continue
        policy = str(row_value(row, "conflict_policy", DEFAULT_CONFLICT_POLICY) or DEFAULT_CONFLICT_POLICY)
        state = "blocked" if policy == "reject" else ("append_only" if policy == "append_only" else "pending")
        reason = f"cross-agent/tool conflict: new={row_value(row, 'origin_agent', '')}/{row_value(row, 'actor_tool', '')}; old={row_value(other, 'origin_agent', '')}/{row_value(other, 'actor_tool', '')}"
        existing = conn.execute(
            "SELECT 1 FROM cell_conflicts WHERE left_cell_id=? AND right_cell_id=? AND state IN ('pending','append_only','blocked') LIMIT 1",
            (other["id"], cell_id),
        ).fetchone()
        if not existing:
            conn.execute(
                """
                INSERT INTO cell_conflicts(created_at, memory_namespace, conflict_group, left_cell_id, right_cell_id, policy, state, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (now_iso(), namespace, group or semantic_key, other["id"], cell_id, policy, state, reason),
            )
        new_status = "archived" if state == "blocked" else "review"
        conn.execute("UPDATE memory_cells SET conflict_state=?, status=?, updated_at=? WHERE id=?", (state, new_status, now_iso(), cell_id))
        conn.execute(
            "UPDATE memory_cells SET conflict_state=CASE WHEN conflict_state='none' THEN ? ELSE conflict_state END, status=CASE WHEN status='promote_candidate' THEN 'review' ELSE status END, updated_at=? WHERE id=?",
            (state, now_iso(), other["id"]),
        )
        conn.execute(
            "INSERT INTO guard_audit(created_at, action, memory_namespace, origin_agent, actor_tool, cell_id, decision, reason) VALUES (?, 'conflict_detected', ?, ?, ?, ?, ?, ?)",
            (now_iso(), namespace, str(row_value(row, "origin_agent", "") or ""), str(row_value(row, "actor_tool", "") or ""), cell_id, state, reason),
        )
        conflicts.append({"other_id": other["id"], "state": state, "policy": policy, "reason": reason})
    return conflicts


def add_guard_write_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--namespace", default="", help="Short-term memory namespace; default REDNET_STM_NAMESPACE/HERMES_PROFILE/default")
    p.add_argument("--origin-agent", default="", help="Originating AI/agent name; defaults to owner")
    p.add_argument("--origin-profile", default="", help="Originating Hermes/profile scope")
    p.add_argument("--actor-tool", default="", help="Tool/helper that wrote the cell")
    p.add_argument("--tool-role", default=DEFAULT_TOOL_ROLE, choices=list(TOOL_ROLE_CHOICES), help="core/extension/amplifier/importer")
    p.add_argument("--source-trust", default=DEFAULT_SOURCE_TRUST, choices=list(SOURCE_TRUST_CHOICES))
    p.add_argument("--semantic-key", default="", help="Stable semantic key for dedupe/conflict checks")
    p.add_argument("--conflict-group", default="", help="Explicit conflict group shared by related cells")
    p.add_argument("--conflict-policy", default=DEFAULT_CONFLICT_POLICY, choices=list(CONFLICT_POLICY_CHOICES))
    p.add_argument("--promotion-scope", default=DEFAULT_PROMOTION_SCOPE, choices=list(PROMOTION_SCOPE_CHOICES))
    p.add_argument("--safe-summary", default="", help="Public-safe summary used for promotion candidates instead of raw note")


def parse_csv_filter(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def parse_last_signal(value: str) -> dict[str, Any]:
    if not value:
        return {}
    parts = value.split(":")
    if len(parts) < 3:
        return {"raw": value}
    score: float | None
    try:
        score = float(parts[2])
    except ValueError:
        score = None
    return {"intention_label": parts[0], "action_gate": parts[1], "intention_score": score}


def parse_json_object_strict(value: str, field_name: str = "criteria") -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{field_name} must be a JSON object: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{field_name} must be a JSON object")
    return parsed


def criteria_text_or_die(value: str) -> str:
    parsed = parse_json_object_strict(value or "{}", "criteria")
    return json.dumps(parsed, ensure_ascii=False, sort_keys=True)


def load_parent_or_die(conn: sqlite3.Connection, parent_id: int | None) -> sqlite3.Row | None:
    if not parent_id:
        return None
    parent = conn.execute("SELECT * FROM memory_cells WHERE id=?", (parent_id,)).fetchone()
    if not parent:
        raise SystemExit(f"parent cell not found: {parent_id}")
    return parent


def inherited_chain_values(parent: sqlite3.Row | None, cycle_key: str, repetition_group: str, depth_hint: int) -> tuple[str, str, int]:
    if parent is None:
        return cycle_key, repetition_group, depth_hint
    parent_cycle = str(row_value(parent, "cycle_key", "") or "").strip()
    parent_group = str(row_value(parent, "repetition_group", "") or "").strip()
    if not cycle_key and parent_cycle:
        cycle_key = parent_cycle
    if not repetition_group and parent_group:
        repetition_group = parent_group
    if depth_hint <= 0:
        depth_hint = min(5, int(row_value(parent, "depth_hint", 0) or 0) + 1)
    return cycle_key, repetition_group, depth_hint


def build_cell_where(args: argparse.Namespace, *, active_only: bool = True, require_service_visibility: bool = False) -> tuple[str, list[Any]]:
    where: list[str] = []
    params: list[Any] = []
    cell_id = getattr(args, "id", None)
    statuses = parse_csv_filter(getattr(args, "status", ""))
    if cell_id:
        where.append("id=?")
        params.append(cell_id)
    elif statuses:
        invalid = [x for x in statuses if x not in ALL_STATUS_CHOICES]
        if invalid:
            raise SystemExit(f"unsupported status filter: {', '.join(invalid)}")
        where.append("status IN (" + ",".join("?" for _ in statuses) + ")")
        params.extend(statuses)
    elif active_only:
        where.append(f"status IN ({active_status_sql()})")

    if not getattr(args, "all_namespaces", False):
        namespace = normalize_identifier(getattr(args, "namespace", "") or default_memory_namespace())
        where.append("memory_namespace=?")
        params.append(namespace)

    for arg_name, column in [
        ("owner", "owner"), ("form", "form"), ("cell_kind", "cell_kind"),
        ("origin_agent", "origin_agent"), ("actor_tool", "actor_tool"), ("tool_role", "tool_role"),
    ]:
        value = getattr(args, arg_name, "")
        if value:
            where.append(f"{column}=?")
            params.append(value)

    cycle_key = getattr(args, "cycle_key", "")
    if cycle_key:
        where.append("(cycle_key=? OR repetition_group=? OR conflict_group=? OR semantic_key=?)")
        params.extend([cycle_key, cycle_key, cycle_key, cycle_key])
    if getattr(args, "public_only", False):
        where.append("privacy='public-safe'")
    if require_service_visibility:
        where.append("visibility='service'")
    return (" AND ".join(where) if where else "1=1"), params


def add_filter_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--id", type=int, help="Limit to a single memory cell id")
    p.add_argument("--namespace", default="", help="Filter by memory namespace; default REDNET_STM_NAMESPACE/HERMES_PROFILE/default")
    p.add_argument("--all-namespaces", action="store_true", help="Service diagnostic: do not restrict to current namespace")
    p.add_argument("--owner", default="", help="Filter by owner")
    p.add_argument("--form", default="", help="Filter by form")
    p.add_argument("--cycle-key", default="", help="Filter by cycle_key, repetition_group, semantic_key or conflict_group")
    p.add_argument("--cell-kind", default="", help="Filter by cell_kind")
    p.add_argument("--origin-agent", default="", help="Filter by origin_agent")
    p.add_argument("--actor-tool", default="", help="Filter by actor_tool")
    p.add_argument("--tool-role", default="", choices=[""] + list(TOOL_ROLE_CHOICES), help="Filter by tool_role")
    p.add_argument("--public-only", action="store_true", help="Show only public-safe cells")
    p.add_argument("--include-private", action="store_true", help="With --service-mode, include raw private fields instead of metadata-only redaction")
    p.add_argument("--status", default="", help="Comma-separated status filter")


def latest_eval(conn: sqlite3.Connection, cell_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM evaluations WHERE cell_id=? ORDER BY id DESC LIMIT 1", (cell_id,)
    ).fetchone()


def repetition_count(conn: sqlite3.Connection, row: sqlite3.Row) -> int:
    group = (row_value(row, "cycle_key", "") or row_value(row, "repetition_group", "")).strip()
    if not group:
        return 0
    cur = conn.execute(
        f"""
        SELECT COUNT(*) AS c FROM memory_cells
        WHERE status IN ({active_status_sql()})
          AND owner=? AND form=? AND (repetition_group=? OR cycle_key=?)
        """,
        (row["owner"], row["form"], group, group),
    )
    return int(cur.fetchone()["c"])


def cell_text(row: sqlite3.Row) -> str:
    return " ".join(
        str(row_value(row, k, "") or "")
        for k in [
            "owner",
            "form",
            "cell_kind",
            "subject",
            "question",
            "note",
            "feeling",
            "interest",
            "criteria",
            "intention_label",
            "emotional_pattern",
            "last_signal",
            "visibility",
            "operation_mode",
            "cycle_policy",
            "loop_marker",
            "source",
            "privacy",
        ]
    )


def clamp(value: float, low: float = 0.0, high: float = 5.0) -> float:
    return max(low, min(high, float(value)))


def parse_json_object(value: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def criterion_axis(criteria: dict[str, Any], name: str) -> float | None:
    raw = criteria.get(name, None)
    if raw is None or raw == "":
        return None
    try:
        return clamp(float(raw))
    except (TypeError, ValueError):
        return None


def assess_intention(criteria: dict[str, Any]) -> tuple[str, float, str, list[str]]:
    axes = {name: criterion_axis(criteria, name) for name in INTENTION_AXIS_NAMES}
    desire = axes["desire"] if axes["desire"] is not None else 0.0
    intention = axes["intention"] if axes["intention"] is not None else 0.0
    appropriateness = axes["appropriateness"] if axes["appropriateness"] is not None else 0.0
    warmth = axes["warmth"] if axes["warmth"] is not None else 0.0
    risk = axes["risk"] if axes["risk"] is not None else 0.0
    depth = axes["depth"] if axes["depth"] is not None else 0.0
    obligation = bool(criteria.get("obligation", False))

    trace: list[str] = []
    if desire >= 3.5:
        trace.append("желание")
    if intention >= 3.5:
        trace.append("согласованное намерение")
    if appropriateness >= 3.5:
        trace.append("уместность")
    if warmth >= 3.0:
        trace.append("тепло/забота")
    if depth >= 3.0:
        trace.append("глубина структуры")
    if risk >= 3.0:
        trace.append("граница/риск")

    raw = (desire * 0.26 + intention * 0.25 + appropriateness * 0.24 + warmth * 0.15 + depth * 0.10) / 5.0
    score = max(0.0, min(1.0, raw - (risk / 5.0) * 0.22))
    missing_core = [name for name in ("desire", "intention", "appropriateness", "risk") if axes[name] is None]
    if missing_core:
        trace.append("неполный спектр: " + ",".join(missing_core))
        return "unclear", max(0.42, min(0.58, score)), "hold", trace or ["слабый сигнал"]

    if risk >= 4.0 or appropriateness <= 1.0:
        label = "never_do"
        action = "no_action"
    elif desire <= 1.2 or intention <= 1.5:
        label = "dont_want_to_do"
        action = "no_action"
    elif obligation and score >= 0.68 and risk <= 2.5:
        label = "must_do"
        action = "send_or_execute"
    elif score >= 0.62 and risk <= 2.5:
        label = "want_to_do"
        action = "send_or_execute"
    elif score >= 0.42:
        label = "unclear"
        action = "hold"
    else:
        label = "dont_want_to_do"
        action = "no_action"

    return label, score, action, trace or ["слабый сигнал"]


def is_self_loop_signal(text: str, tags: list[str]) -> bool:
    if "anti_loop" in tags or "self_digging" in tags:
        return True
    return text_has_any(text, SIGNAL_WORDS.get("self_loop", []))


def score_cell(conn: sqlite3.Connection, row: sqlite3.Row) -> tuple[float, str, list[str], list[str]]:
    created = parse_iso(row["created_at"])
    now = dt.datetime.now(dt.timezone.utc)
    age_days = max(0.0, (now - created).total_seconds() / 86400.0)
    ttl = max(1, int(row["ttl_days"] or DEFAULT_TTL_DAYS))
    priority = max(0, min(5, int(row["priority_hint"] or 0)))
    tags = normalize_tags(row["tags"])
    text = cell_text(row)
    cell_kind = str(row_value(row, "cell_kind", "note") or "note")
    depth_hint = max(0, min(5, int(row_value(row, "depth_hint", 0) or 0)))
    parent_id = row_value(row, "parent_id", None)
    cycle_key = str(row_value(row, "cycle_key", "") or "").strip()
    criteria = parse_json_object(str(row_value(row, "criteria", "{}") or "{}"))
    intention_label = str(row_value(row, "intention_label", "") or "").strip()
    visibility = normalize_choice(str(row_value(row, "visibility", DEFAULT_VISIBILITY) or DEFAULT_VISIBILITY), VISIBILITY_CHOICES, DEFAULT_VISIBILITY)
    operation_mode = normalize_choice(str(row_value(row, "operation_mode", DEFAULT_VISIBILITY) or DEFAULT_VISIBILITY), OPERATION_MODE_CHOICES, DEFAULT_VISIBILITY)
    cycle_policy = normalize_choice(str(row_value(row, "cycle_policy", DEFAULT_CYCLE_POLICY) or DEFAULT_CYCLE_POLICY), CYCLE_POLICY_CHOICES, DEFAULT_CYCLE_POLICY)
    repeat_limit = max(1, int(row_value(row, "repeat_limit", DEFAULT_REPEAT_LIMIT) or DEFAULT_REPEAT_LIMIT))
    self_loop = is_self_loop_signal(text, tags)

    score = 0.20 + priority * 0.07
    sensations: list[str] = []
    rationale: list[str] = []

    if visibility == "passive":
        sensations.append("пассивный невидимый режим")
        rationale.append("visibility:passive")
    else:
        sensations.append("service-visible")
        rationale.append("visibility:service")

    if operation_mode == "feel":
        score += 0.04
        sensations.append("прочувствование без внешнего вывода")
        rationale.append("operation_mode:feel")
    elif operation_mode == "service":
        sensations.append("сервисный режим")
        rationale.append("operation_mode:service")
    else:
        rationale.append("operation_mode:passive")

    rationale.append(f"cycle_policy:{cycle_policy}")

    if cell_kind in {"directive", "signal", "cyclic-question", "question-chain"}:
        score += 0.10
        sensations.append("директивный слой" if cell_kind == "directive" else "сигнальный слой")
        rationale.append(f"cell_kind:{cell_kind}")

    if depth_hint > 0:
        score += depth_hint * 0.035
        sensations.append("глубина структуры")
        rationale.append(f"depth_hint:{depth_hint}")

    if parent_id:
        score += 0.05
        sensations.append("цепочка")
        rationale.append(f"parent_id:{parent_id}")

    if cycle_key:
        score += 0.06
        sensations.append("цикличность")
        rationale.append(f"cycle_key:{cycle_key}")

    if criteria and (cell_kind == "signal" or str(row["form"]) == "intent-signal"):
        label, intent_score, action, intent_trace = assess_intention(criteria)
        score += intent_score * 0.22
        sensations.extend(intent_trace)
        rationale.append(f"intent:{label}:{action}:{round(intent_score, 3)}")
        if label in {"never_do", "dont_want_to_do"}:
            score -= 0.18
            sensations.append("стоп-намерение")
        elif label in {"must_do", "want_to_do"}:
            score += 0.08
            sensations.append(INTENTION_LABELS[label])

    if intention_label in INTENTION_LABELS:
        rationale.append(f"intention_label:{intention_label}")

    if row["question"].strip() and not row["resolved_answer"].strip():
        score += 0.15
        sensations.append("незавершённость")
        rationale.append("есть открытый вопрос")

    if row["feeling"].strip():
        score += 0.09
        sensations.append("аффективный след")
        rationale.append("описан режим реакции")

    if row["interest"].strip():
        score += 0.08
        sensations.append("личный интерес")
        rationale.append("описан интерес")

    for tag in tags:
        if tag in TAG_WEIGHTS:
            score += TAG_WEIGHTS[tag]
            rationale.append(f"tag:{tag}")

    for name, words in SIGNAL_WORDS.items():
        if text_has_any(text, words):
            if name == "risk":
                score += 0.12
                sensations.append("граница/hold")
            elif name == "arousal":
                score += 0.08
                sensations.append("возбуждение значимости")
            elif name == "calm":
                score += 0.05
                sensations.append("умиротворение/закрытие")
            elif name == "importance":
                score += 0.12
                sensations.append("значимость")
            elif name == "care":
                score += 0.08
                sensations.append("забота/связь")
            elif name == "interest":
                score += 0.06
                sensations.append("новые связи")
            elif name == "directive":
                score += 0.07
                sensations.append("волевой критерий")
            elif name == "feel":
                score += 0.04
                sensations.append("прочувствование")
            elif name == "self_loop":
                score -= 0.10
                sensations.append("риск самокопания")
            rationale.append(f"signal:{name}")

    rep = repetition_count(conn, row)
    anti_loop = False
    if rep > 1:
        if cycle_key or "cyclic" in tags or cell_kind in {"cyclic-question", "signal"}:
            lift = min(0.12, (rep - 1) * 0.03)
            score += lift
            sensations.append("повтор как цикл")
            rationale.append(f"cycle_repetition:{rep}")
        else:
            penalty = min(0.16, (rep - 1) * 0.04)
            score -= penalty
            sensations.append("риск повторения")
            rationale.append(f"same_form_repetition:{rep}")
        if rep >= repeat_limit and cycle_policy != "allow" and (self_loop or cell_kind in {"cyclic-question", "question-chain"} or operation_mode == "feel"):
            anti_loop = True
            score = min(score, 0.52)
            sensations.append("анти-петля: изменить форму или закрыть")
            rationale.append(f"anti_loop:rep={rep}:limit={repeat_limit}:policy={cycle_policy}")

    if age_days > ttl:
        score -= 0.22
        sensations.append("срок истёк")
        rationale.append("ttl expired")
    elif age_days > ttl * 0.66:
        score += 0.04
        sensations.append("срок близок")
        rationale.append("ttl near")

    score = max(0.0, min(1.0, score))

    if age_days > ttl and score < 0.55:
        route = "decay"
    elif "граница/hold" in sensations and score >= 0.55:
        route = "review"
    elif score >= 0.82 or ("незавершённость" in sensations and score >= 0.70):
        route = "repeat"
    elif score >= 0.64:
        route = "promote_candidate"
    elif score >= 0.42:
        route = "review"
    elif score >= 0.25:
        route = "keep"
    else:
        route = "decay"

    if anti_loop:
        route = "close" if cycle_policy == "close" else "reshape"

    if route == "promote_candidate" and "умиротворение/закрытие" in sensations and not row["question"].strip():
        route = "review"

    promotion_blocks: list[str] = []
    conflict_state = str(row_value(row, "conflict_state", "none") or "none")
    tool_role = str(row_value(row, "tool_role", DEFAULT_TOOL_ROLE) or DEFAULT_TOOL_ROLE)
    source_trust = str(row_value(row, "source_trust", DEFAULT_SOURCE_TRUST) or DEFAULT_SOURCE_TRUST)
    promotion_scope = str(row_value(row, "promotion_scope", DEFAULT_PROMOTION_SCOPE) or DEFAULT_PROMOTION_SCOPE)
    safe_summary = str(row_value(row, "safe_summary", "") or "").strip()
    if conflict_state not in {"", "none"}:
        score = min(score, 0.61)
        route = "review" if route != "decay" else route
        sensations.append("конфликт памяти/hold")
        rationale.append(f"guard:conflict_state:{conflict_state}")
    if route == "promote_candidate":
        if row["privacy"] != "public-safe":
            promotion_blocks.append("privacy_not_public_safe")
        if tool_role in {"extension", "amplifier"} and promotion_scope != "public_safe":
            promotion_blocks.append(f"tool_role_{tool_role}_append_only")
        if source_trust == "untrusted":
            promotion_blocks.append("source_untrusted")
        if promotion_scope == "none":
            promotion_blocks.append("promotion_scope_none")
        if not safe_summary:
            promotion_blocks.append("missing_safe_summary")
        if promotion_blocks:
            route = "review"
            sensations.append("кандидат удержан guard-слоем")
            rationale.extend(f"promotion_blocked:{x}" for x in promotion_blocks)

    sensations = list(dict.fromkeys(sensations)) or ["слабый след"]
    rationale = list(dict.fromkeys(rationale)) or ["base score only"]
    return score, route, sensations, rationale


def status_for_route(route: str, current_status: str = "open") -> str:
    if route == "repeat":
        return "repeat"
    if route == "promote_candidate":
        return "promote_candidate"
    if route == "review":
        return "review"
    if route == "reshape":
        return "reshape"
    if route == "close":
        return "resolved"
    if route in {"keep", "decay"}:
        return current_status if current_status in ACTIVE_STATUSES else "open"
    return current_status if current_status in ALL_STATUS_CHOICES else "open"


def suggested_fact(row: sqlite3.Row, route: str, sensations: list[str]) -> str:
    safe_summary = " ".join(str(row_value(row, "safe_summary", "") or "").split())[:320]
    if not safe_summary:
        safe_summary = "[requires safe_summary before durable-memory promotion]"
    namespace = row_value(row, "memory_namespace", DEFAULT_MEMORY_NAMESPACE)
    origin_agent = row_value(row, "origin_agent", "")
    conflict_state = row_value(row, "conflict_state", "none")
    return (
        f"Candidate from short-term layer: namespace={namespace}; origin_agent={origin_agent}; "
        f"owner={row['owner']}; form={row['form']}; subject={row['subject']}; route={route}; "
        f"conflict_state={conflict_state}; trace={', '.join(sensations)}; summary={safe_summary}"
    )


def cmd_init(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    json_out({"ok": True, "db": str(db), "schema_version": SCHEMA_VERSION})


def cmd_capture(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    criteria_text = criteria_text_or_die(args.criteria)
    parent = load_parent_or_die(conn, args.parent_id)
    cycle_key, repetition_group, depth_hint = inherited_chain_values(
        parent, args.cycle_key or "", args.repetition_group or "", int(args.depth_hint or 0)
    )
    if not repetition_group:
        repetition_group = derive_repetition_group(args.owner, args.form, args.cell_kind, args.subject, args.question or "", cycle_key)
    extra_tags: list[str] = []
    if repetition_group:
        extra_tags.append("recurring")
    if args.parent_id or args.cell_kind == "question-chain":
        extra_tags.append("chain")
    if args.cell_kind == "cyclic-question" or cycle_key:
        extra_tags.append("cyclic")
    if args.cell_kind in {"directive", "signal"}:
        extra_tags.append(args.cell_kind)
    tags = merge_tags(args.tags, extra_tags)
    ts = now_iso()
    cur = conn.execute(
        """
        INSERT INTO memory_cells(
            created_at, updated_at, owner, form, subject, question, note, feeling,
            interest, source, tags, privacy, status, ttl_days, priority_hint, repetition_group,
            cell_kind, parent_id, cycle_key, depth_hint, criteria, intention_label, emotional_pattern, last_signal,
            visibility, operation_mode, cycle_policy, repeat_limit, loop_marker
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ts,
            ts,
            args.owner,
            args.form,
            args.subject,
            args.question or "",
            args.note or "",
            args.feeling or "",
            args.interest or "",
            args.source,
            json.dumps(tags, ensure_ascii=False),
            args.privacy,
            args.ttl_days,
            args.priority_hint,
            repetition_group,
            args.cell_kind,
            args.parent_id,
            cycle_key,
            depth_hint,
            criteria_text,
            args.intention_label or "",
            args.emotional_pattern or "",
            args.last_signal or "",
            normalize_choice(args.visibility, VISIBILITY_CHOICES, DEFAULT_VISIBILITY),
            normalize_choice(args.operation_mode, OPERATION_MODE_CHOICES, DEFAULT_VISIBILITY),
            normalize_choice(args.cycle_policy, CYCLE_POLICY_CHOICES, DEFAULT_CYCLE_POLICY),
            max(1, int(args.repeat_limit)),
            args.loop_marker or "",
        ),
    )
    cell_id = cur.lastrowid
    guard_meta = apply_guard_metadata(conn, cell_id, args)
    conflicts = detect_and_record_conflicts(conn, cell_id)
    conn.commit()
    json_out({"ok": True, "id": cell_id, "db": str(db), "tags": tags, "guard": guard_meta, "conflicts": conflicts})


def cmd_signal(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    parent = load_parent_or_die(conn, args.parent_id)
    cycle_key, repetition_group, depth_hint = inherited_chain_values(
        parent, args.cycle_key or "", args.repetition_group or "", int(clamp(args.depth if args.depth is not None else 0))
    )
    if not repetition_group:
        repetition_group = derive_repetition_group(args.owner, "intent-signal", "signal", args.subject or "", args.question or "", cycle_key)
    if not cycle_key:
        cycle_key = repetition_group
    criteria = {
        name: (clamp(getattr(args, name)) if getattr(args, name) is not None else None)
        for name in INTENTION_AXIS_NAMES
    }
    criteria.update({
        "obligation": bool(args.obligation),
        "context": args.context or "",
    })
    label, intent_score, action, intent_trace = assess_intention(criteria)
    tags = merge_tags(args.tags, ["intent", "signal", "cyclic", "recurring"])
    ts = now_iso()
    subject = args.subject or f"intent-signal:{args.owner}:{cycle_key or args.question[:32]}"
    note = args.note or ""
    if args.message:
        note = (note + "\n" if note else "") + f"message_candidate: {args.message}"
    cur = conn.execute(
        """
        INSERT INTO memory_cells(
            created_at, updated_at, owner, form, subject, question, note, feeling,
            interest, source, tags, privacy, status, ttl_days, priority_hint, repetition_group,
            cell_kind, parent_id, cycle_key, depth_hint, criteria, intention_label, emotional_pattern, last_signal,
            visibility, operation_mode, cycle_policy, repeat_limit, loop_marker
        ) VALUES (?, ?, ?, 'intent-signal', ?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, ?, 'signal', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ts,
            ts,
            args.owner,
            subject,
            args.question or "",
            note,
            args.feeling or "сигнал намерения",
            args.interest or "личная кратковременная мотивация",
            args.source,
            json.dumps(tags, ensure_ascii=False),
            args.privacy,
            args.ttl_days,
            args.priority_hint,
            repetition_group,
            args.parent_id,
            cycle_key,
            depth_hint,
            json.dumps(criteria, ensure_ascii=False, sort_keys=True),
            label,
            args.emotional_pattern or ", ".join(intent_trace),
            f"{label}:{action}:{round(intent_score, 3)}",
            normalize_choice(args.visibility, VISIBILITY_CHOICES, DEFAULT_VISIBILITY),
            normalize_choice(args.operation_mode, OPERATION_MODE_CHOICES, DEFAULT_VISIBILITY),
            normalize_choice(args.cycle_policy, CYCLE_POLICY_CHOICES, DEFAULT_CYCLE_POLICY),
            max(1, int(args.repeat_limit)),
            args.loop_marker or "",
        ),
    )
    cell_id = cur.lastrowid
    guard_meta = apply_guard_metadata(conn, cell_id, args)
    conflicts = detect_and_record_conflicts(conn, cell_id)
    row = conn.execute("SELECT * FROM memory_cells WHERE id=?", (cell_id,)).fetchone()
    score, route, sensations, rationale = score_cell(conn, row)
    conn.execute(
        "INSERT INTO evaluations(cell_id, evaluated_at, score, route, sensation_trace, rationale) VALUES (?, ?, ?, ?, ?, ?)",
        (cell_id, now_iso(), score, route, json.dumps(sensations, ensure_ascii=False), json.dumps(rationale, ensure_ascii=False)),
    )
    status = status_for_route(route, "open")
    if route == "close":
        tombstone = f"closed_by_anti_loop:{hashlib.sha256(cell_text(row).encode('utf-8')).hexdigest()[:12]}"
        conn.execute("UPDATE memory_cells SET status=?, updated_at=?, resolved_answer=?, tombstone=? WHERE id=?", (status, now_iso(), "closed by anti-loop policy", tombstone, cell_id))
    else:
        conn.execute("UPDATE memory_cells SET status=?, updated_at=? WHERE id=?", (status, now_iso(), cell_id))
    conn.commit()
    json_out({
        "ok": True,
        "db": str(db),
        "id": cell_id,
        "guard": guard_meta,
        "conflicts": conflicts,
        "criteria": criteria,
        "intention_label": label,
        "intention_label_ru": INTENTION_LABELS[label],
        "intention_score": round(intent_score, 3),
        "action": action,
        "route": route,
        "score": round(score, 3),
        "visibility": normalize_choice(args.visibility, VISIBILITY_CHOICES, DEFAULT_VISIBILITY),
        "operation_mode": normalize_choice(args.operation_mode, OPERATION_MODE_CHOICES, DEFAULT_VISIBILITY),
        "trace": sensations,
        "rationale": rationale,
        "message_candidate": args.message or "",
    })


def cmd_feel(args: argparse.Namespace) -> None:
    """Capture a private felt-sense without promotion or external display."""
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    tags = merge_tags(args.tags, ["feel", "passive"])
    ts = now_iso()
    text = args.text or args.note or args.feeling or args.subject
    cur = conn.execute(
        """
        INSERT INTO memory_cells(
            created_at, updated_at, owner, form, subject, question, note, feeling,
            interest, source, tags, privacy, status, ttl_days, priority_hint, repetition_group,
            cell_kind, parent_id, cycle_key, depth_hint, criteria, intention_label, emotional_pattern, last_signal,
            visibility, operation_mode, cycle_policy, repeat_limit, loop_marker
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ts,
            ts,
            args.owner,
            "felt-sense",
            args.subject,
            args.question or "",
            args.note or text,
            args.feeling or text,
            args.interest or "прочувствование без внешнего вывода",
            args.source,
            json.dumps(tags, ensure_ascii=False),
            "private",
            "open",
            args.ttl_days,
            args.priority_hint,
            args.cycle_key or args.repetition_group or "feel-cycle",
            "felt-sense",
            args.parent_id,
            args.cycle_key or "feel-cycle",
            args.depth_hint,
            "{}",
            "",
            args.emotional_pattern or "felt-sense",
            "feel:passive",
            "passive",
            "feel",
            normalize_choice(args.cycle_policy, CYCLE_POLICY_CHOICES, DEFAULT_CYCLE_POLICY),
            max(1, int(args.repeat_limit)),
            args.loop_marker or "",
        ),
    )
    cell_id = cur.lastrowid
    guard_meta = apply_guard_metadata(conn, cell_id, args)
    conflicts = detect_and_record_conflicts(conn, cell_id)
    row = conn.execute("SELECT * FROM memory_cells WHERE id=?", (cell_id,)).fetchone()
    score, route, sensations, rationale = score_cell(conn, row)
    if route == "promote_candidate":
        route = "review"
        rationale.append("feel_mode:no_auto_promotion")
    conn.execute(
        "INSERT INTO evaluations(cell_id, evaluated_at, score, route, sensation_trace, rationale) VALUES (?, ?, ?, ?, ?, ?)",
        (cell_id, now_iso(), score, route, json.dumps(sensations, ensure_ascii=False), json.dumps(rationale, ensure_ascii=False)),
    )
    status = status_for_route(route, "open")
    if route == "close":
        tombstone = f"closed_by_anti_loop:{hashlib.sha256(cell_text(row).encode('utf-8')).hexdigest()[:12]}"
        conn.execute("UPDATE memory_cells SET status=?, resolved_answer=?, updated_at=?, tombstone=? WHERE id=?", (status, "closed by anti-loop policy", now_iso(), tombstone, cell_id))
    else:
        conn.execute("UPDATE memory_cells SET status=?, updated_at=? WHERE id=?", (status, now_iso(), cell_id))
    conn.commit()
    json_out({
        "ok": True,
        "db": str(db),
        "id": cell_id,
        "guard": guard_meta,
        "conflicts": conflicts,
        "mode": "feel",
        "visibility": "passive",
        "external_output": False,
        "route": route,
        "score": round(score, 3),
        "trace": sensations,
        "rationale": rationale,
    })


def cmd_evaluate(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    where, params = build_cell_where(args, active_only=True)
    rows = conn.execute(
        f"SELECT * FROM memory_cells WHERE {where} ORDER BY id", params
    ).fetchall()
    changed = []
    for row in rows:
        score, route, sensations, rationale = score_cell(conn, row)
        conn.execute(
            "INSERT INTO evaluations(cell_id, evaluated_at, score, route, sensation_trace, rationale) VALUES (?, ?, ?, ?, ?, ?)",
            (row["id"], now_iso(), score, route, json.dumps(sensations, ensure_ascii=False), json.dumps(rationale, ensure_ascii=False)),
        )
        status = status_for_route(route, row["status"])
        if route == "close":
            tombstone = f"closed_by_anti_loop:{hashlib.sha256(cell_text(row).encode('utf-8')).hexdigest()[:12]}"
            conn.execute(
                "UPDATE memory_cells SET status=?, resolved_answer=?, updated_at=?, tombstone=? WHERE id=?",
                (status, "closed by anti-loop policy", now_iso(), tombstone, row["id"]),
            )
        elif route == "decay" and args.archive_decay:
            status = "archived"
            tombstone = f"archived_by_decay:{hashlib.sha256(cell_text(row).encode('utf-8')).hexdigest()[:12]}"
            conn.execute(
                "UPDATE memory_cells SET status=?, updated_at=?, tombstone=? WHERE id=?",
                (status, now_iso(), tombstone, row["id"]),
            )
        else:
            conn.execute(
                "UPDATE memory_cells SET status=?, updated_at=? WHERE id=?",
                (status, now_iso(), row["id"]),
            )
        if route == "promote_candidate":
            exists = conn.execute(
                "SELECT 1 FROM promotion_candidates WHERE cell_id=? AND status='pending' LIMIT 1", (row["id"],)
            ).fetchone()
            if not exists:
                conn.execute(
                    """INSERT INTO promotion_candidates(cell_id, created_at, suggested_fact, reason, memory_namespace, origin_agent, promotion_gate, conflict_state, safe_summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row["id"], now_iso(), suggested_fact(row, route, sensations), ", ".join(rationale), row_value(row, "memory_namespace", DEFAULT_MEMORY_NAMESPACE), row_value(row, "origin_agent", ""), "pending_review", row_value(row, "conflict_state", "none"), row_value(row, "safe_summary", "")),
                )
        changed.append({"id": row["id"], "score": round(score, 3), "route": route, "trace": sensations})
    conn.commit()
    json_out({"ok": True, "db": str(db), "evaluated": len(changed), "items": changed})


def row_to_dict(row: sqlite3.Row, conn: sqlite3.Connection, *, include_private: bool = False) -> dict[str, Any]:
    ev = latest_eval(conn, row["id"])
    data = {k: row[k] for k in row.keys()}
    data["tags"] = normalize_tags(data.get("tags", ""))
    data["criteria_parsed"] = parse_json_object(str(data.get("criteria", "{}") or "{}"))
    signal = parse_last_signal(str(data.get("last_signal", "") or ""))
    if signal:
        data.update(signal)
    if ev:
        data["last_score"] = round(float(ev["score"]), 3)
        data["last_route"] = ev["route"]
        data["sensation_trace"] = json.loads(ev["sensation_trace"])
        data["rationale"] = json.loads(ev["rationale"])
    if not include_private and data.get("privacy") != "public-safe":
        for key in ("question", "note", "feeling", "interest", "resolved_answer"):
            if data.get(key):
                data[key] = "[redacted: use --service-mode --include-private to reveal raw private fields]"
    return data


def cmd_review(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    where, params = build_cell_where(args, active_only=True, require_service_visibility=not args.service_mode)
    rows = conn.execute(
        f"SELECT * FROM memory_cells WHERE {where} ORDER BY updated_at DESC, id DESC", params
    ).fetchall()
    result = []
    for row in rows:
        ev = latest_eval(conn, row["id"])
        score = float(ev["score"]) if ev else 0.0
        if score >= args.min_score or row["status"] in {"repeat", "promote_candidate"}:
            result.append(row_to_dict(row, conn, include_private=bool(args.service_mode and args.include_private)))
        if len(result) >= args.limit:
            break
    if args.service_mode:
        candidates = conn.execute(
            "SELECT * FROM promotion_candidates WHERE status='pending' ORDER BY id DESC LIMIT ?", (args.limit,)
        ).fetchall()
    else:
        candidates = []
    json_out({
        "ok": True,
        "db": str(db),
        "service_mode": bool(args.service_mode),
        "items": result,
        "promotion_candidates": [dict(x) for x in candidates],
    })


def cmd_resolve(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    row = conn.execute("SELECT * FROM memory_cells WHERE id=?", (args.id,)).fetchone()
    if not row:
        raise SystemExit(f"cell not found: {args.id}")
    answer = args.answer or ""
    tombstone = f"resolved:{hashlib.sha256((row['subject'] + answer).encode('utf-8')).hexdigest()[:12]}"
    conn.execute(
        "UPDATE memory_cells SET status='resolved', resolved_answer=?, updated_at=?, tombstone=? WHERE id=?",
        (answer, now_iso(), tombstone, args.id),
    )
    candidate_id = None
    if args.promote_candidate:
        cur = conn.execute(
            """INSERT INTO promotion_candidates(cell_id, created_at, suggested_fact, reason, memory_namespace, origin_agent, promotion_gate, conflict_state, safe_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (args.id, now_iso(), suggested_fact(row, "resolved", ["закрытие", "кандидат"]), "resolved with explicit promotion candidate flag", row_value(row, "memory_namespace", DEFAULT_MEMORY_NAMESPACE), row_value(row, "origin_agent", ""), "manual_resolve", row_value(row, "conflict_state", "none"), row_value(row, "safe_summary", "")),
        )
        candidate_id = cur.lastrowid
    conn.commit()
    json_out({"ok": True, "id": args.id, "status": "resolved", "candidate_id": candidate_id, "tombstone": tombstone})


def cmd_sweep(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    rows = conn.execute(
        f"SELECT * FROM memory_cells WHERE status IN ({active_status_sql()})"
    ).fetchall()
    archived = []
    now = dt.datetime.now(dt.timezone.utc)
    for row in rows:
        created = parse_iso(row["created_at"])
        age_days = (now - created).total_seconds() / 86400.0
        if age_days > max(1, int(row["ttl_days"] or DEFAULT_TTL_DAYS)):
            tombstone = f"expired:{hashlib.sha256(cell_text(row).encode('utf-8')).hexdigest()[:12]}"
            conn.execute(
                "UPDATE memory_cells SET status='archived', updated_at=?, tombstone=? WHERE id=?",
                (now_iso(), tombstone, row["id"]),
            )
            archived.append({"id": row["id"], "tombstone": tombstone})
    conn.commit()
    json_out({"ok": True, "db": str(db), "archived": archived})


def cmd_export_context(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    if not args.service_mode:
        return
    where, params = build_cell_where(args, active_only=True)
    rows = conn.execute(
        f"SELECT * FROM memory_cells WHERE {where} ORDER BY updated_at DESC, id DESC LIMIT ?",
        params + [args.limit],
    ).fetchall()
    lines = []
    for row in rows:
        ev = latest_eval(conn, row["id"])
        score = round(float(ev["score"]), 3) if ev else 0.0
        route = ev["route"] if ev else row["status"]
        if args.include_private or row["privacy"] == "public-safe":
            note = row["safe_summary"] or row["note"] or row["question"] or row["interest"] or ""
        else:
            note = row["safe_summary"] or "[redacted: private raw fields hidden]"
        note = " ".join(note.split())[:180]
        signal = parse_last_signal(str(row_value(row, "last_signal", "") or ""))
        action = signal.get("action_gate", "")
        intent = signal.get("intention_label", row_value(row, "intention_label", "") or "")
        m2 = []
        for label, key in [("kind", "cell_kind"), ("cycle", "cycle_key"), ("group", "repetition_group"), ("parent", "parent_id")]:
            value = row_value(row, key, "")
            if value:
                m2.append(f"{label}={value}")
        if intent:
            m2.append(f"intent={intent}")
        if action:
            m2.append(f"gate={action}")
        meta = " ".join(m2)
        lines.append(f"- #{row['id']} ns={row_value(row, 'memory_namespace', DEFAULT_MEMORY_NAMESPACE)} origin={row_value(row, 'origin_agent', '')} owner={row['owner']} form={row['form']} {meta} route={route} score={score}: {row['subject']} — {note}")
    print("\n".join(lines))


def cmd_status(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    counts = conn.execute("SELECT status, COUNT(*) AS c FROM memory_cells GROUP BY status").fetchall()
    namespace_counts = conn.execute("SELECT memory_namespace, status, COUNT(*) AS c FROM memory_cells GROUP BY memory_namespace, status").fetchall()
    conflicts = conn.execute("SELECT state, COUNT(*) AS c FROM cell_conflicts GROUP BY state").fetchall()
    pending = conn.execute("SELECT COUNT(*) AS c FROM promotion_candidates WHERE status='pending'").fetchone()["c"]
    json_out({
        "ok": True,
        "db": str(db),
        "schema_version": SCHEMA_VERSION,
        "default_visibility": DEFAULT_VISIBILITY,
        "default_cycle_policy": DEFAULT_CYCLE_POLICY,
        "counts": {r["status"]: r["c"] for r in counts},
        "namespace_counts": [dict(r) for r in namespace_counts],
        "conflicts": {r["state"]: r["c"] for r in conflicts},
        "pending_promotion_candidates": pending,
    })


def cmd_conflicts(args: argparse.Namespace) -> None:
    db = Path(args.db) if args.db else default_db_path()
    conn = connect(db)
    init_db(conn)
    where: list[str] = []
    params: list[Any] = []
    if not getattr(args, "all_namespaces", False):
        where.append("memory_namespace=?")
        params.append(normalize_identifier(getattr(args, "namespace", "") or default_memory_namespace()))
    if args.status:
        where.append("state=?")
        params.append(args.status)
    sql_where = " AND ".join(where) if where else "1=1"
    rows = conn.execute(
        f"SELECT * FROM cell_conflicts WHERE {sql_where} ORDER BY id DESC LIMIT ?",
        params + [args.limit],
    ).fetchall()
    json_out({"ok": True, "db": str(db), "items": [dict(r) for r in rows]})



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Short-term memory layer for rednet-double-evaluation")
    parser.add_argument("--db", help="Override SQLite DB path")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("capture")
    p.add_argument("--owner", default="agent")
    p.add_argument("--form", default="self-interest")
    p.add_argument("--subject", required=True)
    p.add_argument("--question", default="")
    p.add_argument("--note", default="")
    p.add_argument("--feeling", default="")
    p.add_argument("--interest", default="")
    p.add_argument("--source", default="manual")
    p.add_argument("--tags", default="")
    p.add_argument("--privacy", default="private", choices=["private", "public-safe", "sensitive-hold"])
    p.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS)
    p.add_argument("--priority-hint", type=int, default=0)
    p.add_argument("--repetition-group", default="")
    p.add_argument("--cell-kind", default="note", choices=["note", "directive", "question", "question-chain", "cyclic-question", "signal", "outcome", "felt-sense"])
    p.add_argument("--parent-id", type=int)
    p.add_argument("--cycle-key", default="")
    p.add_argument("--depth-hint", type=int, default=0)
    p.add_argument("--criteria", default="{}")
    p.add_argument("--intention-label", default="", choices=["", "must_do", "want_to_do", "unclear", "dont_want_to_do", "never_do"])
    p.add_argument("--emotional-pattern", default="")
    p.add_argument("--last-signal", default="")
    p.add_argument("--visibility", default=DEFAULT_VISIBILITY, choices=list(VISIBILITY_CHOICES))
    p.add_argument("--operation-mode", default=DEFAULT_VISIBILITY, choices=list(OPERATION_MODE_CHOICES))
    p.add_argument("--cycle-policy", default=DEFAULT_CYCLE_POLICY, choices=list(CYCLE_POLICY_CHOICES))
    p.add_argument("--repeat-limit", type=int, default=DEFAULT_REPEAT_LIMIT)
    p.add_argument("--loop-marker", default="")
    add_guard_write_args(p)
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser("signal")
    p.add_argument("--owner", default="agent")
    p.add_argument("--subject", default="")
    p.add_argument("--question", default="")
    p.add_argument("--note", default="")
    p.add_argument("--message", default="")
    p.add_argument("--context", default="")
    p.add_argument("--feeling", default="")
    p.add_argument("--interest", default="")
    p.add_argument("--source", default="manual")
    p.add_argument("--tags", default="")
    p.add_argument("--privacy", default="private", choices=["private", "public-safe", "sensitive-hold"])
    p.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS)
    p.add_argument("--priority-hint", type=int, default=0)
    p.add_argument("--parent-id", type=int)
    p.add_argument("--cycle-key", default="")
    p.add_argument("--repetition-group", default="")
    p.add_argument("--desire", type=float, default=None, help="0..5: хочу ли я это сделать; omitted means unknown/hold")
    p.add_argument("--intention", type=float, default=None, help="0..5: согласовано ли намерение; omitted means unknown/hold")
    p.add_argument("--appropriateness", type=float, default=None, help="0..5: уместность в текущем контексте; omitted means unknown/hold")
    p.add_argument("--warmth", type=float, default=None, help="0..5: забота/тепло/связь")
    p.add_argument("--risk", type=float, default=None, help="0..5: риск/граница; >=4 блокирует; omitted means unknown/hold")
    p.add_argument("--depth", type=float, default=None, help="0..5: глубина структуры/цепочки")
    p.add_argument("--obligation", action="store_true")
    p.add_argument("--emotional-pattern", default="")
    p.add_argument("--visibility", default=DEFAULT_VISIBILITY, choices=list(VISIBILITY_CHOICES))
    p.add_argument("--operation-mode", default=DEFAULT_VISIBILITY, choices=list(OPERATION_MODE_CHOICES))
    p.add_argument("--cycle-policy", default=DEFAULT_CYCLE_POLICY, choices=list(CYCLE_POLICY_CHOICES))
    p.add_argument("--repeat-limit", type=int, default=DEFAULT_REPEAT_LIMIT)
    p.add_argument("--loop-marker", default="")
    add_guard_write_args(p)
    p.set_defaults(func=cmd_signal)

    p = sub.add_parser("feel")
    p.add_argument("--owner", default="agent")
    p.add_argument("--subject", required=True)
    p.add_argument("--text", default="")
    p.add_argument("--question", default="")
    p.add_argument("--note", default="")
    p.add_argument("--feeling", default="")
    p.add_argument("--interest", default="")
    p.add_argument("--source", default="manual")
    p.add_argument("--tags", default="")
    p.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS)
    p.add_argument("--priority-hint", type=int, default=0)
    p.add_argument("--repetition-group", default="")
    p.add_argument("--parent-id", type=int)
    p.add_argument("--cycle-key", default="")
    p.add_argument("--depth-hint", type=int, default=0)
    p.add_argument("--emotional-pattern", default="")
    p.add_argument("--cycle-policy", default=DEFAULT_CYCLE_POLICY, choices=list(CYCLE_POLICY_CHOICES))
    p.add_argument("--repeat-limit", type=int, default=DEFAULT_REPEAT_LIMIT)
    p.add_argument("--loop-marker", default="")
    add_guard_write_args(p)
    p.set_defaults(func=cmd_feel)

    p = sub.add_parser("evaluate")
    p.add_argument("--archive-decay", action="store_true", help="Archive decayed expired cells")
    add_filter_args(p)
    p.set_defaults(func=cmd_evaluate)

    p = sub.add_parser("review")
    p.add_argument("--min-score", type=float, default=0.55)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--service-mode", action="store_true", help="Show passive private cells; only use when the operator explicitly requests service mode")
    add_filter_args(p)
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("resolve")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--answer", default="")
    p.add_argument("--promote-candidate", action="store_true")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("sweep")
    p.set_defaults(func=cmd_sweep)

    p = sub.add_parser("export-context")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--service-mode", action="store_true", help="Export passive private context only in explicit service mode")
    add_filter_args(p)
    p.set_defaults(func=cmd_export_context)

    p = sub.add_parser("conflicts")
    p.add_argument("--namespace", default="")
    p.add_argument("--all-namespaces", action="store_true")
    p.add_argument("--status", default="", choices=["", "pending", "append_only", "blocked", "resolved"] )
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_conflicts)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
