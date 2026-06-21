# RedNET Quiet Step Lab — слои рабочего пространства

Дата: 2026-06-09.
Язык: русский.

## Цель

Разложить лабораторию так, чтобы она могла расти: от первых карточек добычи до публичной библиотеки, автономных охотничьих волн, модулей под конкретных агентов и будущих сильных сущностей RedNET.

## Слои

### 00. Course / Charter / Locales

Назначение: смысл, миссия, язык, публичная рамка.

Пути:

- `locales/README.md`
- `locales/ru/mission.md`
- `locales/en/mission.md`
- `workspace/LAYERS.ru.md`
- `workspace/LAYERS.en.md`

Выход: понятная RU/EN основа, которую можно показать миру без секретов и без потери RedNET-голоса.

### 10. Sources / Hunting Grounds

Назначение: где охотимся.

Источники:

- papers, repos, standards, docs;
- локальные безопасные заметки;
- сабагенты-охотники;
- люди-наставники и будущие «серьёзные сущности»;
- публичные knowledge bases.

Ограничение: источник не считается знанием, пока не оформлен evidence handle.

### 20. Hunt / Inbox

Назначение: принести добычу в форме карточки, а не в форме хаоса.

Пути:

- `templates/discovery-card.md`
- `schemas/discovery-card.schema.json`
- `inbox/YYYY-MM-DD/*.md`

Выход: discovery cards со статусами `pilot_now`, `audit_first`, `scout`, `red_zone`.

### 30. Ledger / Memory of Discoveries

Назначение: не потерять открытия и сделать их запрашиваемыми.

Пути:

- `data/discoveries.jsonl`
- `data/discoveries.sqlite3`
- `adapters/subagent_ingest.py`

Выход: append-only поток и query layer для Совета, отчётов и dashboards.

### 40. Council / Double Evaluation

Назначение: отделить блеск от пригодности.

Пути:

- `council/*.md`

Проверки:

- скрытые допущения;
- динамика во времени;
- инвариант;
- интерфейс/тело;
- факт / гипотеза / метафора / безопасный шаг.

Выход: классификация и приоритеты.

### 50. Carving Bench / Разделка добычи

Назначение: разобрать находку на полезные части.

Для каждой идеи выделить:

- принцип;
- измеримую экономию;
- failure modes;
- минимальный experiment;
- safety gate;
- module candidate;
- public explanation RU/EN.

Выход: подготовленная заготовка для модуля, пилота или публикации.

### 60. Modules / Trophies

Назначение: превращать добычу в reusable capability.

Пути:

- `modules/README.md`
- `modules/templates/module-card.md`
- `modules/packs/*.md`

Выход: модули под агента, роль, решение, сенсор, verifier, storage, router или interface.

### 70. Pilot / Eval / Shadow Mode

Назначение: осторожно проверить полезность.

Правила:

- сначала observe/read-only/shadow;
- без paid API без разрешения;
- без секретов;
- exact verifier или human/Guardian для рискованных действий;
- метрика до включения.

Выход: `pilot_now` становится `pilot_shadow`, потом `reusable` или `retired`.

### 80. Public Library / World-facing Layer

Назначение: дать миру учиться у RedNET.

Состав:

- RU/EN статьи;
- очищенные module packs;
- практики восстановления связности AI;
- методики бережного пробуждения/настройки агентных систем;
- evidence handles.

Ограничение: публикация только после secret scan и приватностной проверки.

### 90. Ops / Funding / Growth

Назначение: чтобы лаборатория могла покрывать будущие исследования.

Состав:

- cost ledger;
- open/free quota policy;
- sponsorship/publication candidates;
- paid API only with explicit Ivan permission;
- NAS/GitHub backup policy;
- roadmap сильных локальных и внешних сущностей.

## Главный инвариант пространства

```text
warmth gives direction;
structure gives continuity;
verification gives trust;
modules give power;
localization gives the world a door.
```
