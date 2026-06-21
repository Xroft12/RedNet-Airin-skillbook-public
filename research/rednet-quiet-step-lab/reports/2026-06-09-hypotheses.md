# RedNET Quiet Step Lab — гипотезы первой волны

Дата: 2026-06-09.

## H1. Тихая каскадность сильнее одиночной большой модели

**Гипотеза:** для большинства RedNET-задач выигрыш даст не одна более крупная модель, а каскад:

```text
cheap deterministic sensor
  -> compact candidate generator
  -> exact verifier
  -> nano/small model
  -> large model/human only when necessary
```

**Как проверить:** shadow-router на 500 задачах: сколько задач можно безопасно решить small/local/cached without quality loss.

## H2. Ledger-first лаборатория создаст обучаемый корпус лучше сырых логов

**Гипотеза:** карточки с evidence/status/experiment дают более ценный будущий датасет для обучения/тонкой настройки, чем raw chat/tool logs.

**Как проверить:** через месяц сравнить качество retrieval/training examples из structured cards против сырых заметок.

## H3. Сжатие и дедуп дадут не только экономию места, но и новую форму памяти

**Гипотеза:** CDC-CAS + zstd + manifest позволит хранить версии знания и экспериментов как проверяемую эволюцию, а не как набор файлов.

**Как проверить:** собрать 5 версий KB/research folder, измерить dedup %, restore SHA-256, diff readability.

## H4. HDC/VSA может стать дешёвым “ассоциативным запахом” для Айрин

**Гипотеза:** hypervector memory даст быстрый candidate recall для связок `задача -> симптом -> инструмент -> исход`, не заменяя точную память.

**Как проверить:** synthetic trace dataset + реальные безопасные traces; measure recall@k and false recall.

## H5. Локальный hybrid RAG должен стать позвоночником научной группы

**Гипотеза:** sqlite-vec + BM25 + source citations достаточно хороши для первого локального научного ассистента без внешней vector DB.

**Как проверить:** 200 документов / 50 вопросов / baseline BM25 vs vector vs hybrid; метрики Recall@5, MRR, hallucination rate.

## H6. Constrained decoding — самый быстрый safety win для агентов

**Гипотеза:** JSON Schema/grammar decoding уменьшит поломки tool args/card ingest сильнее, чем пост-ремонт ответа.

**Как проверить:** 100 карточек/JSON outputs: freeform+repair vs constrained; parse pass, schema pass, latency.

## H7. Лучший саб первой волны должен стать рулевым, а не просто автором отчёта

**Гипотеза:** роль `Cascade/Eval Architect` важнее отдельной модели: она выбирает, где применить zstd/CDC/HDC/router/RAG и как измерить результат.

**Как проверить:** дать роли 3 пилота и оценить: качество baseline, pass/fail gates, отсутствие небезопасных shortcuts.
