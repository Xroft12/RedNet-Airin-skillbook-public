# Runtime data layer

Этот каталог создаётся ingest-адаптером.

Файлы:

- `discoveries.jsonl` — append-only ledger локальной рабочей сессии.
- `discoveries.sqlite3` — query ledger для Совета/отчётов.

В публичную GitHub-ветку эти runtime-файлы не добавляются из-за `.gitignore` (`*.jsonl`, `*.sqlite3`).

Восстановление первой волны:

```bash
python research/rednet-quiet-step-lab/adapters/seed_wave1.py
```

После запуска seed-скрипт создаст Markdown-карточки, JSONL, SQLite и council export. Если карточки уже существуют, не запускай seed повторно без очистки runtime-слоя: текущая версия адаптера append-only и создаст дубликаты.
