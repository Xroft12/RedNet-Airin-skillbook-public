#!/usr/bin/env python3
"""Validate the rednet-double-evaluation package.

Uses only Python stdlib so it can run on a minimal Hermes host.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "manifest.yaml",
    "docs/double-evaluation-meta-skill.md",
    "skills/rednet/rednet-double-evaluation/SKILL.md",
    "skills/rednet/rednet-double-evaluation/references/activation-protocol.md",
    "skills/rednet/rednet-double-evaluation/references/manifestation-protocol.md",
    "skills/rednet/rednet-double-evaluation/references/safety-and-boundaries.md",
    "skills/rednet/rednet-double-evaluation/references/short-term-memory-layer.md",
    "skills/rednet/rednet-double-evaluation/templates/double-evaluation-session-log.md",
    "skills/rednet/rednet-double-evaluation/templates/agent-activation-card.md",
    "skills/rednet/rednet-double-evaluation/templates/short-term-memory-note.md",
    "skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py",
    "install/INSTALL-HERMES.md",
    "install/activation.snippet.md",
    "install/install_hermes_skill.py",
    "checks/validate_package.py",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)access_token\s*[:=]\s*['\"]?[A-Za-z0-9._-]{12,}"),
    re.compile(r"(?i)password\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(skill_text: str) -> tuple[dict[str, str], str]:
    if not skill_text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter at byte 0")
    marker = skill_text.find("\n---\n", 4)
    if marker == -1:
        fail("SKILL.md frontmatter closing marker not found")
    fm_text = skill_text[4:marker]
    body = skill_text[marker + len("\n---\n"):]
    data: dict[str, str] = {}
    for line in fm_text.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key:
            data[key] = value
    return data, body


def validate_required_files() -> None:
    missing = [p for p in REQUIRED_FILES if not (PACKAGE_ROOT / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_skill() -> None:
    skill_path = PACKAGE_ROOT / "skills/rednet/rednet-double-evaluation/SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    for key in ["name", "description", "version", "author", "license"]:
        if key not in fm or not fm[key]:
            fail(f"SKILL.md missing frontmatter key: {key}")
    if fm["name"] != "rednet-double-evaluation":
        fail("SKILL.md name must be rednet-double-evaluation")
    if len(fm["name"]) > 64:
        fail("SKILL.md name exceeds 64 chars")
    if len(fm["description"]) > 1024:
        fail("SKILL.md description exceeds 1024 chars")
    if not body.strip():
        fail("SKILL.md body is empty")
    if len(text) > 100_000:
        fail("SKILL.md exceeds 100,000 chars")


def validate_links() -> None:
    skill_dir = PACKAGE_ROOT / "skills/rednet/rednet-double-evaluation"
    expected = [
        "references/activation-protocol.md",
        "references/manifestation-protocol.md",
        "references/safety-and-boundaries.md",
        "references/short-term-memory-layer.md",
        "templates/double-evaluation-session-log.md",
        "templates/agent-activation-card.md",
        "templates/short-term-memory-note.md",
        "scripts/short_term_memory.py",
    ]
    for rel in expected:
        if not (skill_dir / rel).exists():
            fail(f"linked file missing: {rel}")


def validate_short_term_script() -> None:
    script = PACKAGE_ROOT / "skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py"
    text = script.read_text(encoding="utf-8")
    required_terms = ["promotion_candidates", "memory_cells", "promote_candidate", "export-context", "sweep"]
    for term in required_terms:
        if term not in text:
            fail(f"short_term_memory.py missing expected term: {term}")


def scan_secrets() -> None:
    text_exts = {".md", ".yaml", ".yml", ".py", ".txt"}
    for path in PACKAGE_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_exts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret pattern in {path.relative_to(PACKAGE_ROOT)}")


def main() -> None:
    validate_required_files()
    validate_skill()
    validate_links()
    validate_short_term_script()
    scan_secrets()
    print("OK: rednet-double-evaluation package validated")


if __name__ == "__main__":
    main()
