# RedNET Quiet Step Lab — backlog экспериментов

Статусы: `new`, `ready`, `running`, `done`, `blocked`, `archived`.

## Pilot now

### P1. `redpack-jsonl`: Zstd dictionaries for Hermes/KB JSONL

- **Идея:** сортировка ключей + zstd dictionaries per corpus.
- **Baseline:** raw, gzip, zstd no dict.
- **Metrics:** compression ratio, decode MB/s, random record latency, roundtrip SHA-256.
- **Gate:** выигрыш по размеру без потери roundtrip и без заметного ухудшения latency.
- **Status:** new.

### P2. `quiet-cas`: CDC + zstd + SQLite manifest

- **Идея:** content-defined chunks для версий KB/logs; CAS-хранилище блоков.
- **Baseline:** полные копии папки / обычный zip.
- **Metrics:** dedup %, total size, restore byte-identical, rebuild time.
- **Gate:** restore в staging совпадает по SHA-256.
- **Status:** new.

### P3. `ef-roar-index`: compact postings index

- **Идея:** FST/MARISA dictionary + Elias-Fano/Roaring postings.
- **Baseline:** SQLite FTS5 / JSON arrays.
- **Metrics:** index size, p95 query latency, AND/OR correctness.
- **Gate:** doc set равен baseline, размер/latency лучше на выбранной метрике.
- **Status:** new.

### P4. `quiet-sketch-sensor`: Count-Min / HLL telemetry

- **Идея:** сенсор пишет sketch summaries вместо raw потока.
- **Baseline:** raw event counts in SQLite.
- **Metrics:** memory, top-k accuracy, false alert, bandwidth.
- **Gate:** top-k heavy hitters совпадают с baseline в пределах ошибки.
- **Status:** new.

### P5. `rednet-hdc-memory`: VSA/HDC associative memory

- **Идея:** кодировать `module⊗symptom + action⊗outcome` в bipolar vectors.
- **Baseline:** keyword search / SQLite exact lookup.
- **Metrics:** recall@k, false recall, capacity, latency.
- **Gate:** не используется для действий; только candidate recall.
- **Status:** new.

### P6. `jl-lsh-case-router`: random projection + LSH + exact verify

- **Идея:** быстро искать похожие инциденты без embedding API.
- **Baseline:** full scan TF-IDF / BM25.
- **Metrics:** recall@10, query latency, storage.
- **Gate:** exact verifier подтверждает кандидатов.
- **Status:** new.

### P7. `semantic-cache-shadow`: SQLite semantic cache in shadow mode

- **Идея:** кэш не отвечает, а только измеряет потенциальные hits.
- **Baseline:** no cache.
- **Metrics:** hit candidate rate, false hit rate, stale risk.
- **Gate:** action/tool prompts не кэшируются.
- **Status:** new.

### P8. `onnx-risk-router`: small classifier before LLM

- **Идея:** sklearn/ONNX классифицирует risk/action/cache/small/large/human.
- **Baseline:** всё идёт в LLM.
- **Metrics:** false negative on risky prompts, latency, routing regret.
- **Gate:** classifier может только escalate/block, не исполнять.
- **Status:** new.

## Audit first

### A1. KV-cache compression / eviction

- **Risk:** потеря критичных токенов в safety/code/legal/security tasks.
- **Safe path:** только read-only QA на frozen long-context dataset.

### A2. DSPy optimizer

- **Risk:** оптимизация плохой метрики закрепит плохое поведение.
- **Safe path:** train/dev/test, frozen eval, no production self-training.

### A3. QLoRA/adapters

- **Risk:** overfit и safety regression.
- **Safe path:** только очищенная разметка, ручной gate, feature flag.
