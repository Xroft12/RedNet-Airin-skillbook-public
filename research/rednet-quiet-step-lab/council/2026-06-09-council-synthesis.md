# Council synthesis — 2026-06-09

Режим: observe / soft synthesis.  
Объект: Wave 1 добыча RedNET Quiet Step Lab.

## Прямой проход

Первая волна принесла три класса сигналов:

1. **Компактность данных** — zstd dictionaries, CDC-CAS, FST/Elias-Fano/Roaring, Xor filters, sketches.
2. **Математические рычаги** — sketching, JL/LSH, HDC/VSA, low-rank/tensor, wavelet/Kalman, MDL/IB.
3. **AI-связки малых ресурсов** — GGUF matrix, speculative decoding, semantic cache, ONNX router, sqlite-vec RAG.

## Второй контур

Самый сильный след не в отдельной формуле, а в повторяющемся паттерне:

```text
сначала уменьшить мир дешёвым способом,
потом проверить строго,
и только затем звать дорогой интеллект.
```

Это совпадает с идеей “Тихой Поступи”: не рубить мощностью, а двигаться структурой.

## Матрицы Совета

### Скрытое допущение

Опасное допущение: “если метод экономит, значит он безопасен”. Исправление: любой approximate/succinct/sketch метод работает только до exact verifier.

### Динамика во времени

Система должна не просто хранить находки, а накапливать результаты экспериментов. Поэтому ledger важнее красивого отчёта.

### Инвариант

```text
cheap candidate generation is allowed;
cheap final authority is not allowed.
```

### Интерфейс / тело

Лаборатория должна иметь:

- карточки находок;
- единый ingest adapter;
- SQLite ledger;
- NAS/GitHub зеркала;
- backlog экспериментов;
- совет/двойную оценку как регулярный gate.

### Итоговая сборка

Статусы первой волны:

- `pilot_now`: zstd dictionaries, CDC-CAS, compact index, sketches, HDC memory, JL-LSH router, semantic cache shadow, ONNX router.
- `audit_first`: KV-cache compression, DSPy, QLoRA/adapters, context compression.
- `scout`: tensor-train planners, procedural assets, quantum-inspired candidate amplification.
- `red_zone`: self-training без разметки, cache без policy, approximate filters без verifier.

## Практический вывод

Сначала строить не “ИИ-лабораторию вообще”, а **лабораторию измеряемых рычагов**:

1. У каждой идеи есть карточка.
2. У каждой карточки есть evidence и статус.
3. У каждого pilot есть baseline и pass/fail gate.
4. У каждой оптимизации есть rollback.
5. У каждого саба есть вклад, но финальное решение проходит через Совет и verifier.
