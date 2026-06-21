# RedNET Quiet Step Lab — карта лаборатории

Дата сборки: 2026-06-09.

## 1. Главный контур

```text
subagents / humans / public sources
  -> discovery templates
  -> adapters/subagent_ingest.py (local/private run)
  -> curated reports
  -> council synthesis
  -> workspace/*
  -> backlog/experiments.md
  -> pipelines/*
  -> modules/*
  -> locales/ru + locales/en
  -> pilot prototypes
```

## 2. Где что лежит

- `README.md` — назначение лаборатории и быстрый старт.
- `PROCESS.md` — правила научной охоты, роли, статусы и критерии добычи.
- `locales/` — RU/EN публичная языковая рамка и миссия.
- `workspace/` — слои рабочего пространства лаборатории.
- `pipelines/` — автономные процессы охоты, добычи, разделки и трофеев.
- `templates/discovery-card.md` — шаблон карточки.
- `templates/wave-launch-card.md` — шаблон запуска автономной волны.
- `templates/carving-note.md` — шаблон разделки добычи.
- `templates/trophy-card.md` — шаблон трофея как reusable capability.
- `schemas/discovery-card.schema.json` — минимальная JSON-схема карточки.
- `adapters/subagent_ingest.py` — локальный ingest: Markdown + JSONL + SQLite; результаты raw-run не публикуются.
- `adapters/seed_wave1.py` — воспроизводимая загрузка первой волны.
- raw `inbox/`, `data/*.jsonl`, `data/*.sqlite3` и ledger exports — локальные рабочие слои, не часть публичного репозитория.
- `council/2026-06-09-council-synthesis.md` — ручной синтез Совета + двойной оценки.
- `council/2026-06-09-council-double-evaluation.md` — финальная классификация Совета + второй контур.
- `reports/2026-06-09-wave1-digest.md` — читабельный дайджест первой волны.
- `reports/2026-06-09-hypotheses.md` — рабочие гипотезы лаборатории.
- `backlog/experiments.md` — первые проверочные эксперименты.
- `modules/` — кузница модулей под конкретного агента, роль или решение.

## 3. Статусы карточек Wave 1

- `pilot_now`: 16 — можно безопасно проверять локально/в shadow-mode.
- `audit_first`: 6 — нужна проверка качества/безопасности перед пилотом.
- `scout`: 3 — исследовательские идеи с потенциалом, но пока без прямого внедрения.
- `red_zone`: 1 — принцип можно изучать, но runtime-путь запрещён.

## 4. Постоянные роли научной группы

- `Cascade/Eval Architect` — главный рулевой: строит каскады cheap sensor -> exact verifier -> model/human.
- `Compression Archivist` — отвечает за zstd/CDC/CAS/succinct indexes.
- `Math Lever Hunter` — отвечает за проекции, sketching, HDC, Bayesian/Kalman, low-rank.
- `Nano-LLM Systems Engineer` — отвечает за GGUF, router, constrained decoding, local RAG.
- `Safety/Verifier Keeper` — не даёт approximate структурам стать финальной истиной.

## 5. Инварианты

```text
approximate structures may reduce search space;
only exact verifier / frozen eval / human gate may authorize high-risk action.
```

```text
small models and sketches are sensors;
ledger and verification are memory;
large model is expensive synthesis, not default reflex.
```

```text
RU/EN localization is not decoration;
it is the public interface by which the lab can teach the world without leaking private context.
```

## 6. Первый рекомендуемый pilot bundle

1. `redpack-jsonl`: Zstd dictionaries for Hermes/KB JSONL.
2. `quiet-cas`: FastCDC + BLAKE3 CAS snapshots.
3. `hybrid-local-rag`: sqlite-vec + BM25 + citations.
4. `schema-safe-output`: constrained decoding for tool/card JSON.
5. `shadow-router`: ONNX/sklearn risk router + semantic cache in shadow mode.

## 7. Красные перила

- Никаких raw секретов в карточках, JSONL, SQLite, GitHub или NAS mirror.
- Никакого self-training на собственных сырых ответах.
- Никакой semantic cache выдачи ответа без shadow precision audit.
- Никакого quantum-washing: quantum-inspired != quantum speedup.
- Никакой approximate filter/projection/sketch как финальный decision maker.
