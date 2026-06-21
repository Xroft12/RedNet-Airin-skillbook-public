#!/usr/bin/env python3
"""RedNET Quiet Step Lab subagent ingest adapter.

Unified layer for subagent discoveries:
- inbox/YYYY-MM-DD/*.md cards
- data/discoveries.jsonl append-only ledger
- data/discoveries.sqlite3 query ledger

Safe by default: redacts secret-like strings before persistence.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Iterable

STATUSES = {"candidate", "pilot_now", "audit_first", "scout", "red_zone"}
KINDS = {"algorithm", "formula", "architecture", "prototype", "risk", "source", "experiment", "other"}

SECRET_PATTERNS = [
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+\-/=]{12,}"),
    re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password|passwd|pwd)\s*[:=]\s*)([^\s,;]{4,})"),
    re.compile(r"(?i)(Authorization\s*[:=]\s*)([^\n\r]{8,})"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def lab_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def redact(text: str) -> str:
    out = text
    for pat in SECRET_PATTERNS:
        def repl(m: re.Match[str]) -> str:
            return m.group(1) + "[redacted-secret-like-value]"
        out = pat.sub(repl, out)
    return out


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9а-яё]+", "-", value, flags=re.IGNORECASE)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:80] or "discovery"


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def ensure_dirs(base: Path) -> None:
    for rel in ["data", "inbox", "reports", "council", "backlog", "templates", "schemas", "adapters"]:
        (base / rel).mkdir(parents=True, exist_ok=True)


def connect(base: Path) -> sqlite3.Connection:
    db = base / "data" / "discoveries.sqlite3"
    conn = sqlite3.connect(db)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS discoveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            role TEXT NOT NULL,
            kind TEXT NOT NULL,
            status TEXT NOT NULL,
            title TEXT NOT NULL,
            tags_json TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            source TEXT NOT NULL,
            card_path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            summary TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_discoveries_status ON discoveries(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_discoveries_kind ON discoveries(kind)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_discoveries_created ON discoveries(created_at)")
    conn.commit()
    return conn


def cmd_init(args: argparse.Namespace) -> int:
    base = Path(args.base).resolve() if args.base else lab_root_from_script()
    ensure_dirs(base)
    connect(base).close()
    print(f"initialized: {base}")
    return 0


def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.summary_file:
        return Path(args.summary_file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --text, --summary-file, or stdin")


def cmd_ingest(args: argparse.Namespace) -> int:
    base = Path(args.base).resolve() if args.base else lab_root_from_script()
    ensure_dirs(base)
    if args.status not in STATUSES:
        raise SystemExit(f"Invalid status {args.status!r}; expected one of {sorted(STATUSES)}")
    if args.kind not in KINDS:
        raise SystemExit(f"Invalid kind {args.kind!r}; expected one of {sorted(KINDS)}")

    created_at = now_iso()
    body = redact(read_input(args).strip())
    title = redact(args.title.strip())
    role = redact(args.role.strip())
    source = redact(args.source or "subagent")
    tags = split_csv(args.tags)
    evidence = split_csv(args.evidence)
    digest_source = json.dumps({"title": title, "role": role, "body": body, "created_at": created_at}, ensure_ascii=False)
    sha = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()

    day = created_at[:10]
    inbox_dir = base / "inbox" / day
    inbox_dir.mkdir(parents=True, exist_ok=True)
    card_name = f"{day}-{slugify(title)}-{sha[:8]}.md"
    card_path = inbox_dir / card_name

    frontmatter = {
        "title": title,
        "role": role,
        "kind": args.kind,
        "status": args.status,
        "tags": tags,
        "evidence": evidence,
        "source": source,
        "created_at": created_at,
        "sha256": sha,
    }
    md = "---\n" + json.dumps(frontmatter, ensure_ascii=False, indent=2) + "\n---\n\n" + body + "\n"
    card_path.write_text(md, encoding="utf-8")

    record = {
        **frontmatter,
        "card_path": str(card_path.relative_to(base)).replace(os.sep, "/"),
        "summary": body[:4000],
    }
    jsonl = base / "data" / "discoveries.jsonl"
    with jsonl.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    conn = connect(base)
    conn.execute(
        """
        INSERT INTO discoveries(created_at, role, kind, status, title, tags_json, evidence_json, source, card_path, sha256, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            role,
            args.kind,
            args.status,
            title,
            json.dumps(tags, ensure_ascii=False),
            json.dumps(evidence, ensure_ascii=False),
            source,
            record["card_path"],
            sha,
            body[:4000],
        ),
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(json.dumps({"id": new_id, "card": record["card_path"], "sha256": sha}, ensure_ascii=False))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    base = Path(args.base).resolve() if args.base else lab_root_from_script()
    conn = connect(base)
    sql = "SELECT id, created_at, status, kind, role, title, card_path FROM discoveries"
    params: list[object] = []
    if args.status:
        sql += " WHERE status = ?"
        params.append(args.status)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(args.limit)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    for row in rows:
        print(f"#{row[0]} [{row[2]}:{row[3]}] {row[5]} — {row[4]} ({row[6]})")
    return 0


def cmd_export_council(args: argparse.Namespace) -> int:
    base = Path(args.base).resolve() if args.base else lab_root_from_script()
    ensure_dirs(base)
    conn = connect(base)
    rows = conn.execute(
        "SELECT id, status, kind, role, title, evidence_json, card_path, summary FROM discoveries ORDER BY status, id"
    ).fetchall()
    conn.close()
    grouped: dict[str, list[tuple]] = {s: [] for s in ["pilot_now", "audit_first", "scout", "red_zone", "candidate"]}
    for row in rows:
        grouped.setdefault(row[1], []).append(row)
    lines = ["# Council export from discovery ledger", "", f"Generated: {now_iso()}", ""]
    for status, status_rows in grouped.items():
        if not status_rows:
            continue
        lines += [f"## {status}", ""]
        for row in status_rows:
            evidence = json.loads(row[5]) if row[5] else []
            lines += [
                f"### #{row[0]} {row[4]}",
                f"- Kind: `{row[2]}`",
                f"- Role: `{row[3]}`",
                f"- Card: `{row[6]}`",
                f"- Evidence: {', '.join(evidence) if evidence else 'requires_verification'}",
                "",
                row[7].strip()[:1200],
                "",
            ]
    out = base / "council" / f"{dt.date.today().isoformat()}-ledger-export.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"exported: {out}")
    return 0


def ignore_for_mirror(dirpath: str, names: Iterable[str]) -> set[str]:
    blocked = {".git", "__pycache__", ".pytest_cache"}
    return {n for n in names if n in blocked or n.endswith(".pyc")}


def cmd_mirror_nas(args: argparse.Namespace) -> int:
    base = Path(args.base).resolve() if args.base else lab_root_from_script()
    target = Path(args.target)
    if not str(target).startswith("\\\\"):
        raise SystemExit("NAS target must be an explicit UNC path starting with \\\\")
    ensure_dirs(base)
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base, target, dirs_exist_ok=True, ignore=ignore_for_mirror)
    print(f"mirrored: {base} -> {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RedNET Quiet Step Lab ingest adapter")
    parser.add_argument("--base", help="Override lab base directory for tests")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")

    pi = sub.add_parser("ingest")
    pi.add_argument("--role", required=True)
    pi.add_argument("--kind", default="other")
    pi.add_argument("--status", default="candidate")
    pi.add_argument("--title", required=True)
    pi.add_argument("--tags", default="")
    pi.add_argument("--evidence", default="")
    pi.add_argument("--source", default="subagent")
    pi.add_argument("--text")
    pi.add_argument("--summary-file")

    pl = sub.add_parser("list")
    pl.add_argument("--status")
    pl.add_argument("--limit", type=int, default=20)

    sub.add_parser("export-council")

    pm = sub.add_parser("mirror-nas")
    pm.add_argument("--target", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "ingest":
        return cmd_ingest(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "export-council":
        return cmd_export_council(args)
    if args.cmd == "mirror-nas":
        return cmd_mirror_nas(args)
    raise SystemExit(f"unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
