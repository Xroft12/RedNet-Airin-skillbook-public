# RedNET Fast Memory — public outline — RU / EN

> Sanitized architecture extracted from the closed project line. This file is not a deployment package and does not contain private runtime material.

## RU — назначение

**RedNET Fast Memory** — исследовательская линия для быстрой локальной памяти агента. В публичном репозитории она описывается только как архитектурный контур: без рабочих архивов, без локальных журналов, без личных данных и без live-конфигураций.

### Безопасная формула

```text
input note
  -> redactor
  -> deterministic analyzer
  -> memory candidate
  -> digest
  -> limited context preview
  -> approval gate
```

### Публично допустимые компоненты

- read-only wrapper surface;
- dry-run installer idea;
- policy template without live values;
- smoke-test philosophy;
- digest generation;
- context preview only after explicit mode check;
- local-only default;
- no automatic context injection in public demo.

### Режимы

| Mode | Public meaning |
|---|---|
| `off` | no context output |
| `observe` | collect and analyze only |
| `soft` | short safe digest |
| `core-only` | internal signal summary |

### Почему важно для QMeta

Fast Memory закрывает проблему долгих сессий: агенту нужен не сырой дневник, а короткие проверяемые кандидаты памяти. QMeta может использовать такие кандидаты как вход для ветвления, аудита, council review и кристаллизации навыков.

## EN — purpose

**RedNET Fast Memory** is a research line for fast local agent memory. In the public repository it is described only as an architecture layer: no working closed bundles, no local logs, no personal data, and no live configuration.

### Safe formula

```text
input note
  -> redactor
  -> deterministic analyzer
  -> memory candidate
  -> digest
  -> limited context preview
  -> approval gate
```

### Public-safe components

- read-only wrapper surface;
- dry-run installer idea;
- policy template without live values;
- smoke-test philosophy;
- digest generation;
- context preview only after explicit mode check;
- local-only default;
- no automatic context injection in public demo.

### Modes

| Mode | Public meaning |
|---|---|
| `off` | no context output |
| `observe` | collect and analyze only |
| `soft` | short safe digest |
| `core-only` | internal signal summary |

### Why it matters for QMeta

Fast Memory addresses long-session continuity: the agent should not consume a raw diary; it should consume short, auditable memory candidates. QMeta can use those candidates as inputs for branching, audit, council review, and skill crystallization.

## Public next steps

1. Add a synthetic memory dataset.
2. Add a minimal deterministic analyzer.
3. Add a `--dry-run` installer demo.
4. Add tests proving that no context is emitted unless the mode allows it.
5. Add QMeta integration examples using only synthetic memory candidates.
