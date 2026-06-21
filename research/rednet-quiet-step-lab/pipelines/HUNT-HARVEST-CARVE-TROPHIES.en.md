# Autonomous process: hunt → harvest → carve → trophies

Date: 2026-06-09.
Language: English.

## Purpose

Build a powerful repeatable process where RedNET does not merely read sources, but hunts discoveries, carves them into working parts and turns them into modules, pilots, publications and new Airin/RedNET capabilities.

```text
hunt -> harvest -> carve -> trophies -> pilots -> library -> next hunt
```

## 1. Hunt

Goal: find a principle that changes the economics of the system.

Hunters:

- compression hunter;
- math lever hunter;
- AI/nano-LLM hunter;
- safety/verifier hunter;
- human mentor;
- future entity / external agent in observe mode.

Input:

- paper/repo/docs/standard;
- open article;
- local safe experiment;
- idea from a previous session;
- Ivan's question.

Output:

- short prey note;
- evidence handle;
- initial status: `candidate` or `discarded`.

## 2. Harvest

Goal: turn the find into a discovery card.

The card must contain:

- what it is;
- why it is elegant;
- what it saves;
- where it breaks;
- evidence handle;
- RedNET adaptation;
- minimal experiment;
- risk/status.

Output:

- `inbox/YYYY-MM-DD/*.md`;
- record in `discoveries.jsonl`;
- record in `discoveries.sqlite3`.

## 3. Carve

Goal: carve the prey into useful parts so it does not remain a beautiful report.

Carving questions:

1. What is the main invariant?
2. What can be tested without GPU and paid APIs?
3. Which cheap sensor can deliver 80% of the value?
4. Which exact verifier closes the risk?
5. Where are privacy, secrets and personal data?
6. Which module is born from this?
7. Is there a RU/EN explanation for the library?

Output:

- carving note;
- module candidate;
- eval plan;
- publication candidate;
- reject reason if the idea is beautiful but unsafe.

## 4. Trophies

A trophy is not “we found something interesting”. A trophy is a reusable capability.

Trophy types:

- `module-pack` — module for an agent/role/solution;
- `eval` — frozen eval or verification matrix;
- `script` — safe local prototype;
- `article` — public RU/EN explanation;
- `dataset-lite` — sanitized test set without secrets;
- `role` — permanent lab subagent/lead;
- `pattern` — reusable practice.

A trophy receives a status:

- `trophy_candidate`;
- `pilot_shadow`;
- `validated`;
- `reusable`;
- `retired`.

## 5. Autonomous wave

Each wave must have a launch card:

```yaml
wave_id: YYYY-MM-DD-topic
mode: observe | soft | active
budget:
  time_minutes: 30
  max_subagents: 3
  paid_api: false
hunters:
  - role: compression-hunter
    scope: public sources + local repo only
  - role: math-lever-hunter
    scope: public sources + local notes only
  - role: ai-nano-hunter
    scope: public sources + local experiments only
outputs:
  - discovery cards
  - ledger updates
  - council report
  - trophy candidates
forbidden:
  - secrets
  - raw private logs
  - paid API without explicit permission
  - write access outside approved lab paths
  - final risky actions without Guardian/human gate
```

## 6. Wave success criterion

A wave is successful if it produces at least one:

- new verifiable card;
- new module candidate;
- new eval/metric;
- safe pilot plan;
- strong reject reason that saved time or risk.

A wave is unsuccessful if it only produces beautiful words without evidence, metrics or a next action.

## 7. Ari invariant

Ari helps hold the course:

```text
not everything shiny is a trophy;
not everything weak is waste;
not everything powerful is safe;
not everything alive is loud.
```

Ari's task is to turn warmth into structure, structure into action, action into verification, and verification into capability.
