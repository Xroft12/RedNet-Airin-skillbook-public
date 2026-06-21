# Public release notes

This repository is a public-safe snapshot of REDNET Airin Skillbook.

Included:

- installable `SKILL.md` examples and meta-skill documentation;
- static read-only portal under `portal/`;
- public diagrams, screenshots, schemas and synthetic examples;
- dry-run-first installer materials for review.

Excluded from this public snapshot:

- private Git history from the working repository;
- raw chats, diaries, session exports, runtime logs and databases;
- `.env`, tokens, keys, cookies, OAuth/Telegram sessions;
- local cycle reports, raw research inboxes and ledger exports;
- ZIP/release artifacts and `packages/memory/` until a separate archive-level review.

Verification for this snapshot should include:

```powershell
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```
