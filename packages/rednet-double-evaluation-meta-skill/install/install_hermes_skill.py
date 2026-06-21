#!/usr/bin/env python3
"""Install rednet-double-evaluation into a Hermes skills directory.

This script copies only the skill folder. It does not edit config, restart
Hermes, or touch secrets.
"""

from __future__ import annotations

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

SKILL_REL = Path("skills") / "rednet" / "rednet-double-evaluation"
TARGET_REL = Path("skills") / "rednet" / "rednet-double-evaluation"


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_hermes_home(profile: str | None, explicit_home: str | None) -> Path:
    if explicit_home:
        return Path(explicit_home).expanduser().resolve()
    if profile:
        return (Path.home() / ".hermes" / "profiles" / profile).resolve()
    local_app_data = os.environ.get("LOCALAPPDATA")
    if os.name == "nt" and local_app_data:
        return (Path(local_app_data) / "hermes").resolve()
    return (Path.home() / ".hermes").resolve()


def copy_skill(src: Path, dst: Path, *, dry_run: bool, force: bool) -> None:
    if not src.exists():
        raise SystemExit(f"Source skill directory not found: {src}")
    if not (src / "SKILL.md").exists():
        raise SystemExit(f"Source SKILL.md not found: {src / 'SKILL.md'}")

    print(f"source: {src}")
    print(f"target: {dst}")

    if dry_run:
        print("dry-run: no files copied")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = dst.with_name(dst.name + f".backup-{stamp}")
        if not force:
            raise SystemExit(
                f"Target already exists: {dst}\n"
                f"Run with --force to move it to {backup.name} and install the new copy."
            )
        print(f"backup: {backup}")
        shutil.move(str(dst), str(backup))

    shutil.copytree(src, dst)
    print("installed: rednet-double-evaluation")
    print("next: start a fresh Hermes session or reload the skill index")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install rednet-double-evaluation Hermes skill")
    parser.add_argument("--dry-run", action="store_true", help="show target without copying")
    parser.add_argument("--force", action="store_true", help="backup and replace existing target")
    parser.add_argument("--hermes-home", help="explicit Hermes home directory")
    parser.add_argument("--profile", help="install into ~/.hermes/profiles/NAME")
    args = parser.parse_args()

    root = package_root()
    src = root / SKILL_REL
    home = default_hermes_home(args.profile, args.hermes_home)
    dst = home / TARGET_REL
    copy_skill(src, dst, dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
