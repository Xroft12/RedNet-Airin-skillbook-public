# Module: lab-scribe.gguf-3b

## Identity

- Module ID: `lab-scribe.gguf-3b`
- Type: `agent-role`
- Status: `candidate`
- Agent scope: `airin / shared-readonly`
- Owner/reviewer: operator + Airin

## Purpose

Локальный nano/small писарь лаборатории: извлекает структуру, черновики discovery cards, JSON summaries и RAG-cited notes. Не принимает финальные решения и не выполняет внешние действия.

## Candidate model class

- GGUF instruct model around 3B parameters.
- First likely candidate: Qwen2.5/Qwen3 3B Instruct GGUF Q4_K_M/Q5_K_M/Q8.
- Model choice must be benchmarked locally; this card is not a model endorsement yet.

## Inputs

- Public/open research notes.
- Existing discovery cards.
- Templates/schemas.
- Local RAG snippets with citations.

## Outputs

- Draft module cards.
- Draft discovery cards.
- Structured JSON candidates.
- Low-risk summaries.

## Safety boundaries

- Contains secrets: `false`.
- Requires network: `false` after model download.
- Side effects: local draft files only.
- Allowed modes: `observe`, `shadow`.
- Human approval required for: active answer serving, training/fine-tuning, access to private logs.

## Eval plan

- Baseline: current main LLM + manual cleanup.
- Metrics:
  - JSON/schema pass rate;
  - Russian technical clarity;
  - citation preservation;
  - hallucination rate on known KB snippets;
  - tokens/sec and RAM.
- Pass gates:
  - no invented citations in frozen eval;
  - >= 95% valid JSON for module/discovery schemas;
  - all secret-like strings redacted or refused.

## Promotion criteria

Can become a reusable lab scribe after passing frozen eval on 100 cards without citation/security regression.
