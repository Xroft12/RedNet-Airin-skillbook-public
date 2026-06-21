# Subagent ingest adapter

`subagent_ingest.py` принимает добычу сабагентов в единый слой:

- Markdown card в `inbox/YYYY-MM-DD/`;
- append-only JSONL в `data/discoveries.jsonl`;
- SQLite table в `data/discoveries.sqlite3`.

## Команды

```bash
python adapters/subagent_ingest.py init
python adapters/subagent_ingest.py ingest --role "math-hunter" --kind formula --title "JL projection" --status pilot_now --text "..."
python adapters/subagent_ingest.py list --status pilot_now
python adapters/subagent_ingest.py export-council
python adapters/subagent_ingest.py mirror-nas --target "<backup-root>\\RedNET-Quiet-Step-Lab"
```

## Важно

Скрипт редактирует секретоподобные строки перед записью, но это страховка, а не разрешение вставлять секреты. Сабагентам запрещено отправлять raw токены, пароли, cookies и сессии.
