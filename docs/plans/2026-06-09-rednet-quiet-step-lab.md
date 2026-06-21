# RedNET Quiet Step Lab Implementation Plan

> **For Hermes:** Use subagent-driven-development style execution task-by-task. All changes are safe-by-default and secret-free.

**Goal:** Build a professional research-library process for RedNET/Airin scientific scouting: subagent cards, council synthesis, experiment backlog, GitHub-clean structure, and NAS mirror path.

**Architecture:** Markdown cards are human-readable; JSONL is append-only; SQLite is the query layer; council reports synthesize without becoming the source of truth.

**Tech stack:** Python stdlib, SQLite, Markdown, JSONL, Git, optional NAS UNC mirror.

## Phase 1 — Storage and adapter

- Create `research/rednet-quiet-step-lab/`.
- Create `adapters/subagent_ingest.py`.
- Create schema/template/process docs.
- Verify `py_compile`, `init`, `ingest`, `list`, `export-council`.

## Phase 2 — Wave 1 knowledge capture

- Save Wave 1 digest.
- Ingest pilot cards into ledger.
- Generate council export.
- Classify ideas: `pilot_now`, `audit_first`, `scout`, `red_zone`.

## Phase 3 — GitHub + NAS

- Keep GitHub variant sanitized.
- Mirror lab folder to NAS staging path.
- Do not include secrets/raw credentials.
- Do not push GitHub remote unless explicitly approved or confirmed safe.

## Phase 4 — Experiments

- Run `redpack-jsonl` prototype.
- Run `quiet-cas` prototype.
- Run compact index prototype.
- Run HDC memory prototype.
- Run semantic cache shadow prototype.

## Acceptance criteria

- Adapter creates Markdown/JSONL/SQLite records.
- Council export is generated.
- Lab docs exist and are readable.
- NAS mirror succeeds or reports blocker.
- No secrets are printed or stored.
