# Module: shadow-router

## Identity

- Module ID: `shadow-router`
- Type: `router`
- Status: `designed`
- Agent scope: `airin / shared-readonly`
- Owner/reviewer: operator + Airin

## Purpose

Дешёвый риск/стоимость router, который сначала работает только в shadow mode: предсказывает путь `cache/small/large/human/block`, но не управляет реальным ответом до аудита.

## Discovery refs

- `#21 Semantic cache in shadow mode`.
- `#22 ONNX/sklearn risk and cost router`.
- Related: Kalman/Bayesian belief state, LSH candidate cascades.

## Inputs

- Sanitized task metadata.
- Risk features: PII, cyber, code, external side effects, schema need, source count.
- Outcome labels from reviewed runs.

## Outputs

- Shadow prediction logs.
- Calibration report.
- Go/no-go gate for active routing.

## Safety boundaries

- Contains secrets: `false`; only metadata/features.
- Requires network: `false`.
- Side effects: none in shadow.
- Allowed modes: `observe`, `shadow` only until approved.
- Human approval required for: active routing, caching real answers, training on raw chats.

## Eval plan

- Baseline: current manual/LLM routing.
- Metrics:
  - AUROC / macro-F1;
  - expected calibration error;
  - false negative rate on high-risk tasks;
  - p95 inference latency;
  - reviewer disagreement.
- Pass gates:
  - zero critical false negatives in canary set;
  - semantic cache precision manually audited before serving;
  - block/human routes are conservative by default.

## Promotion criteria

Can move from `pilot_shadow` to limited active only after reviewed canary set and operator approval.
