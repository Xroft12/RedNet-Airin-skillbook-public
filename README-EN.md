<div align="center">

<a href="docs/index.md">
  <img src="assets/rednet-banner.svg" alt="REDNET Airin Skillbook banner" width="920">
</a>

# REDNET Airin Skillbook

**Public-safe skillbook for QMeta meta-skills, Airin/Hermes workflows, reproducible research, dry-run tooling and grant-ready open-source maintenance.**

[Русская версия](README-RU.md) · [Documentation](docs/index.md) · [Install](INSTALL.md) · [Skills](docs/skills.md) · [QMeta](docs/qmeta-scientific-model.md) · [Grant Pack](grants/README.md) · [Privacy Boundary](docs/privacy-boundary.md)

</div>

## Overview

REDNET Airin Skillbook is a public-safe open-source repository for agent workflow research and reusable meta-skills. It presents the Airin/Hermes skill system, QMeta branching model, read-only portal materials, dry-run installation logic, release discipline and grant application materials without exposing private runtime state.

The repository is intended for reviewers, maintainers, researchers and collaborators who need to understand the project without access to private infrastructure. It contains documentation, installable skill cards, synthetic examples, diagrams, public protocols and curated research summaries.

## What QMeta is

QMeta is a classical engineering model for meta-skills. It does not claim physical quantum computation, model consciousness, magic or non-local effects. Quantum-information terms are used only as engineering analogies for branching, error correction, ensemble evaluation, threshold behavior and traceable decision memory.

The core process is:

```text
branching -> audit -> score -> council -> interference -> measure -> answer | skill
```

A regular skill helps produce an answer. A meta-skill changes the process itself: criteria, caution level, memory policy, verification mode, branch structure and the decision trace.

![QMeta operator](assets/qmeta-operator.svg)

## Why this repository matters

Modern long-running agent workflows often fail in predictable ways: they lose continuity, mix facts with assumptions, ignore uncertainty or produce work that is hard to audit later. REDNET Airin Skillbook addresses these problems through explicit process controls:

- branching and comparison of multiple solution paths;
- separation of facts, hypotheses, metaphors and actions;
- dry-run first installation and read-only preview modes;
- strict public/private publication boundary;
- reusable skill cards and documented acceptance checks;
- bilingual documentation for international review.

## Reviewer path

For grant, model access or open-source review, read these pages in order:

1. [QMeta / Airin grant positioning](docs/qmeta-grant-positioning.ru-en.md)
2. [OpenAI application drafts](grants/openai-applications.ru-en.md)
3. [Codex Open Source Fund note](grants/openai-codex-fund.md)
4. [Scientific grant radar](grants/scientific-grant-radar.ru-en.md)
5. [Privacy boundary](docs/privacy-boundary.md)
6. [QMeta scientific model](docs/qmeta-scientific-model.md)
7. [Closed archive audit summary](docs/closed-archive-audit-2026-06-27.ru-en.md)

## Repository map

| Section | Purpose |
|---|---|
| `skills/` | Installable and conceptual skills for REDNET / Airin / Hermes workflows. |
| `packages/qmeta/rednet-airin-qmeta/` | Python package and optional MCP server for the QMeta branching engine. |
| `research/rednet-quiet-step-lab/` | Public-safe research pipeline for discovery cards, module packs and experiments. |
| `portal/` | Static read-only PWA showcase. |
| `docs/` | Architecture, navigation, privacy boundary, release checks and QMeta documents. |
| `grants/` | Grant and model-access application pack. |
| `assets/` | Public diagrams, banners, icons and visual maps. |

## Grant and access focus

The repository is prepared for four primary application tracks:

| Track | Request |
|---|---|
| OpenAI Codex for Open Source | ChatGPT Pro with Codex, API credits and maintainer workflow support. |
| OpenAI Codex Open Source Fund | API credits for QMeta evaluations and open-source maintenance. |
| OpenAI Trusted Access / defensive research support | Support for authorized code review, patch validation and maintainer checklists. |
| OpenAI Researcher Access Program | API credits for evaluating QMeta on public-safe synthetic tasks. |

Additional provider and grant options are tracked in [grants/provider-radar.md](grants/provider-radar.md) and [grants/scientific-grant-radar.ru-en.md](grants/scientific-grant-radar.ru-en.md).

## Visual materials

| Asset | Purpose |
|---|---|
| [rednet-banner.svg](assets/rednet-banner.svg) | Main repository banner. |
| [qmeta-operator.svg](assets/qmeta-operator.svg) | QMeta operator diagram. |
| [airin-icon.svg](assets/airin-icon.svg) | Airin visual identity icon. |
| [skillbook-map.svg](assets/skillbook-map.svg) | Repository structure map. |
| [install-flow.svg](assets/install-flow.svg) | Safe installation flow. |

## Quick start

### Dry-run installation

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

The dry-run mode previews planned operations and does not copy files.

### Read-only portal

```powershell
python -m http.server 8795
```

Open:

```text
http://127.0.0.1:8795/portal/
```

## Public boundary

The public repository includes sanitized documentation, diagrams, synthetic examples, installable skill cards, read-only demos, review checklists and grant-facing summaries.

The public repository excludes raw private conversations, personal records, local runtime exports, private infrastructure values, production data, access material and closed archive contents as-is.

See [docs/privacy-boundary.md](docs/privacy-boundary.md) for the canonical boundary.

## Status

This repository is being prepared as a funding-grade public open-source showcase. The goal is to make the project clear, bilingual, auditable and safe for reviewers while keeping private materials outside the public layer.
