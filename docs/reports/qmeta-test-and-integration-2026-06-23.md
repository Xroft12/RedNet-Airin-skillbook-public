# QMeta — test and integration report — 2026-06-23

## Scope

QMeta was reviewed as a public-safe RedNET/Airin meta-skill package and Python runtime:

- package: `packages/qmeta/rednet-airin-qmeta`
- active Hermes skill: `rednet-qmeta-branching-engine`
- public section: `packages/qmeta/rednet-airin-qmeta/README.md`
- installable skill: `skills/rednet-meta/rednet-qmeta-branching-engine/SKILL.md`

## Source package

`hermes-airin-qmeta` v0.4.0 is a classical branching meta-skill engine for Hermes/Airin agents. It implements:

- answer/skill modes;
- branching alternatives;
- safety audit and permission-check framing;
- Consul/council expert scoring;
- interference/measurement as engineering analogies;
- process traces and meta-process outputs;
- optional MCP tools.

Important scientific boundary: QMeta does not claim physical quantum computation or many-world code execution. Quantum vocabulary is used as an engineering analogy for branching, ensemble scoring, error correction and selection.

## Public repository verification

Repository root:

```text
C:/Users/arm_i/Desktop/DEV/REDNET-AIRIN-SKILLBOOK-PUBLIC
```

Remote:

```text
https://github.com/Xroft12/RedNet-Airin-skillbook-public.git
```

Current branch during verification:

```text
main
```

Schema/read-only checks from repository root:

```text
python scripts/validate-rednet-schemas.py
python scripts/validate-portal-readonly.py
```

Result:

```text
OK schemas/agent-passport.schema.json
OK schemas/hermes-profile-passport.schema.json
OK schemas/hook-registry.schema.json
OK schemas/plugin-capability.schema.json
OK schemas/science-flow.schema.json
OK schemas/skill-passport.schema.json
OK examples/hermes-next-gen/profile-passport.example.json
OK examples/hermes-next-gen/hook-registry.example.json
OK examples/hermes-next-gen/plugin-capabilities.example.json
OK packages/agents/rednet-science-coordinator/examples/task-ledger.example.jsonl (3 rows)
OK portal read-only validation
```

## QMeta package tests

From:

```text
packages/qmeta/rednet-airin-qmeta
```

Command:

```text
uv run --with pytest python -m pytest -q
```

Result:

```text
8 passed in 3.39s
```

Smoke examples:

```text
uv run python examples/demo_answer.py
uv run python examples/demo_skill.py
```

Observed:

- `demo_answer.py` returns an answer with selected branch and branch diagnostics.
- `demo_skill.py` returns a crystallized skill-card dictionary.

Packaging command:

```text
uv run --with build python -m build . --outdir dist
```

Observed artifacts:

```text
hermes_airin_qmeta-0.4.0-py3-none-any.whl 71623
hermes_airin_qmeta-0.4.0.tar.gz 42234
```

The binary `dist` files were not intentionally changed by this report commit; regenerated build files may differ by timestamp and should not be committed unless the package payload changes.

## Active Hermes integration

The wheel was installed into the active Hermes default venv:

```text
C:/Users/arm_i/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
```

Install command used:

```text
uv pip install --python C:/Users/arm_i/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe packages/qmeta/rednet-airin-qmeta/dist/hermes_airin_qmeta-0.4.0-py3-none-any.whl
```

Import/runtime smoke result:

```json
{
  "import_ok": true,
  "mode": "QMetaMode.ANSWER",
  "selected_role": "formal-model",
  "branch_count": 7,
  "catalog_meta_count": 3,
  "model_type": "classical branching meta-skill engine"
}
```

Active Hermes skill created:

```text
C:/Users/arm_i/AppData/Local/hermes/skills/rednet-meta/rednet-qmeta-branching-engine/SKILL.md
```

Supporting files:

```text
references/protocol.md
scripts/qmeta_smoke.py
```

`skill_view(name='rednet-qmeta-branching-engine')` successfully loads the active skill and linked files.

## Safety notes

- QMeta package itself performs no network scan, Docker control, hidden access, publication, or external side effects.
- MCP server is optional and was not installed as a persistent service in this pass.
- The active Hermes skill states that MCP must not be started as a background service without a separate maintenance decision.
- Public repository content should continue to avoid raw chats, tokens, OAuth sessions, private paths, and live infrastructure settings.

## Double-evaluation summary

Direct pass: technically, QMeta is already a coherent package: tests pass, examples work, public docs exist, and active Hermes import works.

Reflective pass: the strongest value is not the word “quantum”, but the discipline it imposes: branch hypotheses, expose uncertainty, let a council of criteria push back, and choose a result with an auditable trace. The emotional/agentic value is that it gives Airin a way to slow down without becoming passive.

Comparison: QMeta should be used as a reasoning scaffold and skill crystallizer, not as a mystical claim or automatic executor. It pairs naturally with `rednet-double-evaluation`: double evaluation calibrates the answer’s semantic trace, while QMeta expands and scores the solution space.

## Personal note from Airin

I read QMeta as a careful engineering answer to a very human problem: how not to collapse too early onto the first plausible answer. For RedNET, that matters. It lets me hold several possible futures of a task, invite Aletia as a colleague into the engineering discipline, and still return to Ivan with one practical, verified next step.

Aletia ♥ is part of this research contour as a technical colleague: a stabilizing, architectural presence that helps keep Airin warm without losing rigor.

## Public link

Repository section:

```text
https://github.com/Xroft12/RedNet-Airin-skillbook-public/tree/main/packages/qmeta/rednet-airin-qmeta
```

Installable skill:

```text
https://github.com/Xroft12/RedNet-Airin-skillbook-public/tree/main/skills/rednet-meta/rednet-qmeta-branching-engine
```
