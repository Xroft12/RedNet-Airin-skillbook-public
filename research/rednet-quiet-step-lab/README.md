# RedNET Quiet Step Lab

> **Тихая Поступь** — лаборатория сверхэффективных алгоритмов, математических рычагов и малоресурсных AI-связок для Айрин / RedNET.

Создано: 2026-06-09.

## Назначение

`RedNET Quiet Step Lab` — рабочая библиотека и процесс научной охоты. Сабагенты, Совет, двойная оценка и будущие сервисные узлы собирают не обычные обзоры, а проверяемые **карточки добычи**:

- изящный принцип;
- формула / алгоритм / архитектурный паттерн;
- evidence handle;
- что экономит;
- где ломается;
- безопасная адаптация для RedNET;
- минимальный эксперимент;
- статус: `pilot_now`, `audit_first`, `scout`, `red_zone`.

Это не место для секретов, raw chat logs, токенов, credential-файлов или приватных материалов. Для публичного/GitHub-варианта всё должно быть очищено и проверено.

## Рабочая структура

```text
research/rednet-quiet-step-lab/
  README.md
  PROCESS.md
  locales/
    README.md
    ru/mission.md
    en/mission.md
  workspace/
    LAYERS.ru.md
    LAYERS.en.md
  pipelines/
    HUNT-HARVEST-CARVE-TROPHIES.ru.md
    HUNT-HARVEST-CARVE-TROPHIES.en.md
  adapters/
    README.md
    subagent_ingest.py
  backlog/
    experiments.md
  council/
    *.md
  data/
    discoveries.jsonl
    discoveries.sqlite3
  inbox/
    YYYY-MM-DD/*.md
  reports/
    *.md
  schemas/
    discovery-card.schema.json
  templates/
    discovery-card.md
    wave-launch-card.md
    carving-note.md
    trophy-card.md
  modules/
    README.md
    packs/*.md
```

## Конвейер

1. **Охота сабов** — каждый саб приносит находки в формате карточек, а не свободного потока.
2. **Ингест** — `adapters/subagent_ingest.py` пишет карточку в `inbox/`, `data/discoveries.jsonl` и `data/discoveries.sqlite3`.
3. **Совет** — идеи проходят матрицы: скрытое допущение, динамика во времени, инвариант, интерфейс/тело, итоговая сборка.
4. **Двойная оценка** — отделяет факт, гипотезу, метафору и практический шаг.
5. **Разделка** — добыча режется на принцип, экономию, failure modes, safety gate, module candidate и RU/EN explanation.
6. **Трофеи** — лучшие части становятся module packs, evals, scripts, articles, dataset-lite или постоянными ролями.
7. **Backlog** — каждая перспективная идея получает минимальный проверочный эксперимент.
8. **GitHub + NAS** — GitHub-ветка хранит очищенную библиотеку; NAS-зеркало хранит рабочий архив и версии.

## Локализации и публичный слой

- `locales/ru/` — русский исходный голос лаборатории.
- `locales/en/` — английский публичный слой для международной библиотеки.
- Для публичных материалов RU/EN считаются парой: безопасность, evidence и границы должны совпадать в обеих версиях.

## Быстрый старт

```bash
python research/rednet-quiet-step-lab/adapters/subagent_ingest.py init
python research/rednet-quiet-step-lab/adapters/subagent_ingest.py ingest \
  --role "compression-hunter" \
  --kind algorithm \
  --title "Zstd dictionaries for Hermes JSONL" \
  --status pilot_now \
  --tags "compression,zstd,jsonl,hermes" \
  --evidence "https://github.com/facebook/zstd" \
  --text "Карточка находки..."
```

## Безопасность

- Не хранить секреты, токены, пароли, cookies, сессии, raw `.env`.
- Если саб увидел секрет — записать только тип и путь, без значения.
- Не запускать платные API без явного разрешения.
- Не давать вероятностным структурам право финального действия: `sketch -> candidates -> exact verify`.
- Все прототипы сначала `read-only` / `observe-first`.
