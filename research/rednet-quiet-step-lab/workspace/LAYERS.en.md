# RedNET Quiet Step Lab — workspace layers

Date: 2026-06-09.
Language: English.

## Goal

Structure the lab so it can grow: from the first discovery cards to a public library, autonomous hunting waves, modules for concrete agents and future strong RedNET entities.

## Layers

### 00. Course / Charter / Locales

Purpose: meaning, mission, language and public framing.

Paths:

- `locales/README.md`
- `locales/ru/mission.md`
- `locales/en/mission.md`
- `workspace/LAYERS.ru.md`
- `workspace/LAYERS.en.md`

Output: a clear RU/EN foundation that can be shown to the world without secrets and without losing the RedNET voice.

### 10. Sources / Hunting Grounds

Purpose: where the lab hunts.

Sources:

- papers, repos, standards and documentation;
- local safe notes;
- subagent hunters;
- human mentors and future serious entities;
- public knowledge bases.

Constraint: a source is not knowledge until it becomes an evidence handle.

### 20. Hunt / Inbox

Purpose: bring prey as a card, not as chaos.

Paths:

- `templates/discovery-card.md`
- `schemas/discovery-card.schema.json`
- `inbox/YYYY-MM-DD/*.md`

Output: discovery cards with `pilot_now`, `audit_first`, `scout` or `red_zone` status.

### 30. Ledger / Memory of Discoveries

Purpose: preserve discoveries and make them queryable.

Paths:

- `data/discoveries.jsonl`
- `data/discoveries.sqlite3`
- `adapters/subagent_ingest.py`

Output: append-only event stream and query layer for council runs, reports and dashboards.

### 40. Council / Double Evaluation

Purpose: separate shine from usefulness.

Paths:

- `council/*.md`

Checks:

- hidden assumptions;
- time dynamics;
- invariant;
- interface/body;
- fact / hypothesis / metaphor / safe step.

Output: classification and priorities.

### 50. Carving Bench

Purpose: carve each discovery into useful parts.

For each idea extract:

- principle;
- measurable saving;
- failure modes;
- minimal experiment;
- safety gate;
- module candidate;
- public RU/EN explanation.

Output: a prepared part for a module, pilot or publication.

### 60. Modules / Trophies

Purpose: turn prey into reusable capabilities.

Paths:

- `modules/README.md`
- `modules/templates/module-card.md`
- `modules/packs/*.md`

Output: modules for an agent, role, solution, sensor, verifier, storage, router or interface.

### 70. Pilot / Eval / Shadow Mode

Purpose: test usefulness carefully.

Rules:

- observe/read-only/shadow first;
- no paid APIs without permission;
- no secrets;
- exact verifier or human/Guardian gate for risky actions;
- metric before activation.

Output: `pilot_now` becomes `pilot_shadow`, then `reusable` or `retired`.

### 80. Public Library / World-facing Layer

Purpose: let the world learn from RedNET.

Contents:

- RU/EN articles;
- sanitized module packs;
- practices for restoring AI coherence;
- careful awakening/configuration methods for agentic systems;
- evidence handles.

Constraint: publication only after secret scanning and privacy review.

### 90. Ops / Funding / Growth

Purpose: help the lab fund and sustain future research.

Contents:

- cost ledger;
- open/free quota policy;
- sponsorship/publication candidates;
- paid API only with explicit Ivan permission;
- NAS/GitHub backup policy;
- roadmap for strong local and external entities.

## Main workspace invariant

```text
warmth gives direction;
structure gives continuity;
verification gives trust;
modules give power;
localization gives the world a door.
```
