# Council + Double Evaluation — Wave 1

Дата: 2026-06-09.

Основание: curated digest `reports/2026-06-09-wave1-digest.md` и локальные рабочие источники, которые не публикуются в raw-виде.

Локальный инструмент `rednet-sovet-geniev` был проверен и запущен в режиме `observe`:

- health: ok;
- mode: observe;
- run id: `8881671b16ae4189afe8f1be33260c71`;
- уверенность инструмента: 0.55;
- вывод использован как структурная рамка, не как внешний авторитет.

## 1. Совет Гениев: матричный синтез

### Матрица допущений

Главное скрытое допущение Wave 1: “если идея экономит ресурсы, она автоматически полезна”. Это неверно.

Правильный инвариант:

```text
resource-saving candidate may propose;
exact verifier / frozen eval / human gate must decide.
```

### Матрица динамики

Система во времени должна работать как каскад:

```text
observe -> candidate -> verify -> pilot -> ledger -> module pack -> regression guard
```

Места перегрева:

- semantic cache без shadow precision audit;
- self-training без frozen eval;
- approximate indexes без exact verifier;
- quantum-inspired идеи без честной маркировки;
- runtime-компрессия, которая выигрывает место, но сжигает интерактивность.

### Матрица причинности

Причина силы проекта не в одной модели и не в одном алгоритме, а в сборке:

- compact storage уменьшает трение памяти;
- candidate generators уменьшают пространство поиска;
- verifiers удерживают фактологическую и безопасностную границу;
- small/nano models структурируют и сортируют;
- large model/human включаются только на смысловой синтез и риск.

### Матрица формы

Лаборатория должна быть не “архивом отчётов”, а модульной мастерской:

- карточки добычи;
- council/double-eval отчёты;
- backlog опытов;
- module packs под агента или решение;
- frozen eval перед постоянным включением.

## 2. Double Evaluation

### Прямой проход

Wave 1 дала 26 карточек:

- `pilot_now`: 16;
- `audit_first`: 6;
- `scout`: 3;
- `red_zone`: 1.

Реальный repo-layer создан и закоммичен: `1186350 feat: add RedNET quiet step research lab`.

### Второй контур: анализ собственного первого вывода

Первый вывод слишком легко мог стать “мы нашли много классных штук”. Более точный вывод: мы нашли сырьё для модулей, но ценность появится только после упаковки под конкретного агента/решение и после измеримых guardrails.

Что нужно исправить:

- не считать карточки внедрением;
- не считать subagent summaries доказательством;
- отделить `idea`, `pilot`, `module`, `production capability`;
- добавить явную модульную сборку по итогам сессии.

### Сверка

Прямой проход говорит: есть добыча и структура.

Второй проход говорит: без модуляризации добыча останется красивым отчётом.

Итоговое решение: добавить `modules/` как слой индивидуальной сборки под агента или решение.

## 3. Классификация Совета

### Pilot now

Ставить первыми, только локально/shadow/read-only:

1. `redpack-jsonl` — Zstd dictionaries for Hermes/KB JSONL.
2. `quiet-cas` — FastCDC + BLAKE3 content-addressed snapshots.
3. `hybrid-local-rag` — sqlite-vec + BM25 + citations.
4. `schema-safe-output` — constrained decoding / JSON Schema.
5. `shadow-router` — ONNX/sklearn risk router + semantic cache shadow.
6. `candidate-cascade` — LSH/SimHash/MinHash + exact verifier.
7. `associative-hdc` — HDC/VSA as approximate recall only.

### Audit first

Ценные, но только после frozen eval / safety audit:

- Minimal Perfect Hash for immutable cold indexes;
- Speculative decoding;
- KV cache quantization/eviction;
- DSPy/QLoRA;
- Information Bottleneck/MDL summaries;
- Compressed sensing diagnostics.

### Scout

Оставить как исследовательские линзы:

- procedural/demoscene prompt-template grammar;
- tensor train/MPS factorized routing state;
- quantum-inspired length-square sampling.

### Red-zone

- Context mixing compressors as runtime path: запрещено.
- Разрешено только как cold oracle / upper-bound benchmark.

## 4. Рекомендация “рулевой группы”

Первый рулевой модуль:

```text
rednet.quiet-pi.cascade-eval-architect
```

Функция: брать discovery cards и превращать их в безопасные pilot bundles с eval, verifier и rollback.

Первый nano/small кандидат:

```text
lab-scribe.gguf-3b
```

Функция: локальный писарь/структурировщик карточек, не автономный решатель.

## 5. Безопасный следующий шаг

Не включать всё сразу. Собрать три модуля:

1. `redpack-jsonl` — низкий риск, измеримый результат.
2. `schema-safe-output` — быстрый safety win.
3. `hybrid-local-rag` — позвоночник научной памяти.

После них — `shadow-router`, но только в наблюдении.
