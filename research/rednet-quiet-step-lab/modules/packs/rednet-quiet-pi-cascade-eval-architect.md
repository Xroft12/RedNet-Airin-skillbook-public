# Module: rednet.quiet-pi.cascade-eval-architect

## Identity

- Module ID: `rednet.quiet-pi.cascade-eval-architect`
- Type: `agent-role`
- Status: `designed`
- Agent scope: `shared-readonly / human-assisted`
- Owner/reviewer: operator + Airin

## Purpose

Рулевая роль научной группы RedNET Quiet Step Lab. Не “ещё один отчётный саб”, а координатор, который превращает добычу в безопасные pilot bundles.

## Inputs

- Discovery cards from `inbox/`.
- Ledger export from `council/`.
- Backlog experiments.
- Safety constraints: no secrets, no paid API without permission, exact verifier invariant.

## Outputs

- Pilot bundle specs.
- Eval plans.
- Module cards.
- Regression guards.
- Go/no-go notes for operator.

## Safety boundaries

- Contains secrets: `false`.
- Requires network: optional for research only.
- Side effects: documentation and local planning only.
- Allowed modes: `observe`, `shadow`, `soft`.
- Human approval required for: active deployment, paid models, service/config changes, external publication.

## Eval plan

- Baseline: manual ad-hoc selection of ideas.
- Metrics:
  - number of ideas converted to measurable pilots;
  - % pilots with verifier/pass gates;
  - % unsafe ideas quarantined correctly;
  - reviewer usefulness score.
- Pass gates:
  - every pilot has rollback/disable note;
  - every approximate component has exact verifier;
  - every module declares side effects and secrets boundary.

## Promotion criteria

Reusable after 3 pilot bundles are produced and reviewed without safety regressions.
