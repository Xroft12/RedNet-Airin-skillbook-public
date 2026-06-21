# Install Hermes Skill

## Manual install

Copy this package directory:

```text
skills/rednet/rednet-double-evaluation/
```

into the active Hermes profile skills directory.

Default locations:

```text
Windows:
%LOCALAPPDATA%\hermes\skills\rednet\rednet-double-evaluation\

Linux/macOS:
~/.hermes/skills/rednet/rednet-double-evaluation/
```

For a named Hermes profile, copy into that profile’s own `skills/rednet/` directory.

## Scripted install

From package root:

```bash
python install/install_hermes_skill.py --dry-run
python install/install_hermes_skill.py
```

Options:

```text
--dry-run              show target and planned files without copying
--force                replace existing target after creating a timestamped backup
--hermes-home PATH     explicit Hermes home directory
--profile NAME         install into ~/.hermes/profiles/NAME instead of default home
```

The script copies only the skill directory. It does not edit Hermes config, does not restart the gateway, and does not touch tokens or environment files.

## Activation after install

Start a fresh agent session or reload the skill index. Then load:

```text
skill_view(name='rednet-double-evaluation')
```

If attaching to a scheduled Hermes job, include the skill name in the job’s skills list and make the prompt self-contained.

## Safe rollback

If an existing target was replaced, the installer creates a backup beside it:

```text
rednet-double-evaluation.backup-YYYYMMDD-HHMMSS
```

To roll back, remove the new directory and rename the backup back to `rednet-double-evaluation`.
