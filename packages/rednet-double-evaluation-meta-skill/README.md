# RedNET Double Evaluation Meta-Skill Package

Self-contained release package for adding the `rednet-double-evaluation` meta-skill to a Hermes/RedNET project.

## Contents

```text
rednet-double-evaluation-meta-skill/
  README.md
  manifest.yaml
  docs/
    double-evaluation-meta-skill.md
  skills/
    rednet/
      rednet-double-evaluation/
        SKILL.md
        references/
          activation-protocol.md
          manifestation-protocol.md
          safety-and-boundaries.md
          short-term-memory-layer.md
        templates/
          agent-activation-card.md
          double-evaluation-session-log.md
          short-term-memory-note.md
        scripts/
          short_term_memory.py
  install/
    INSTALL-HERMES.md
    activation.snippet.md
    install_hermes_skill.py
  checks/
    validate_package.py
```

## What the skill does

The skill teaches an agent to:

1. analyze an object directly;
2. analyze its own first analysis as a semantic/affective package;
3. compare both layers;
4. produce the final response in the requested visibility mode;
5. optionally keep unresolved traces in a separate short-term layer named `Кратковременный`;
6. keep short-term cells passive by default, reveal them only through explicit service mode, and reshape or close self-digging loops;
7. protect multi-agent short-term memory with namespace/origin/tool/conflict metadata instead of silently merging traces.

It is a processing protocol, not a claim of human consciousness. It separates fact, observation, interpretation, metaphor, and action.

`Кратковременный` is a separate SQLite helper for temporary attention cells: objects of interest, unresolved questions, gentle reminders, and reaction traces. It does not modify Hermes primary memory or user profile. It only produces review routes, conflict records, and promotion candidates.

Version `1.4.0` adds:

- boundary guards for `memory_namespace`, `origin_agent`, `origin_profile`, `actor_tool`, `tool_role`, `source_trust`, `semantic_key`, `conflict_group`, `conflict_policy`, `promotion_scope`, and `safe_summary`;
- `conflicts` command for reviewing cross-agent/cross-profile/tool boundary events;
- safer extension/amplifier/importer compatibility: tools can write scoped cells, but cannot directly promote raw content to durable memory;
- v1.3 behavior retained: passive visibility by default, `review --service-mode`, `export-context --service-mode`, `feel`, and anti-loop routes `reshape`/`close`.

## Quick install

From the package root:

```bash
python install/install_hermes_skill.py --dry-run
python install/install_hermes_skill.py
```

Or copy manually:

```text
skills/rednet/rednet-double-evaluation/
```

to the target Hermes profile skills directory.

See `install/INSTALL-HERMES.md` for details.

## Activation

In a Hermes task, load the skill and use one of the modes:

- `observe`
- `light`
- `full`
- `manifest`
- `hold`
- `hot-off`
- `short-term`
- `signal`
- `passive`
- `service`
- `feel`

Short trigger:

```text
Примени rednet-double-evaluation: сначала прямой проход, затем второй контур по пакету собственного анализа, потом сверка и только нужный итог.
```

Short-term helper example:

```bash
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py init
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py capture --subject "example" --note "public-safe temporary note" --owner agent --form self-interest --privacy public-safe --visibility passive --namespace agent-a --origin-agent agent-a --semantic-key example --conflict-policy hold --promotion-scope public_safe --safe-summary "public-safe summary"
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py feel --subject "example" --text "quiet felt contour" --namespace agent-a --origin-agent agent-a
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py evaluate --namespace agent-a
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py review --service-mode --namespace agent-a --public-only --min-score 0
python skills/rednet/rednet-double-evaluation/scripts/short_term_memory.py conflicts --namespace agent-a
```

## Validation

Run:

```bash
python checks/validate_package.py
```

The validator checks required files, `SKILL.md` frontmatter, linked references/templates/scripts, and obvious forbidden secret-like patterns.

## Public boundary

This package intentionally contains only sanitized method documentation. It does not include raw chats, private source corpora, secrets, cookies, tokens, workplace/private data, or recoverable details of a closed RedNET runtime.
