# Low-resource memory and routing pack — RU / EN

> Public-safe aggregation of closed Quiet Step Lab cards. Raw inbox cards are not copied; this pack keeps only sanitized principles and experiment ideas.

## RU — зачем пакет

Этот module pack усиливает заявку на API/model credits: он показывает, что REDNET Airin/QMeta не просто просит мощные модели, а умеет экономить контекст, память, сеть и вычисления.

## RU — принципы

| Principle | Public experiment | Value |
|---|---|---|
| Zstd dictionaries for JSONL | Train small dictionaries on synthetic logs and compare size/latency. | cheaper storage and faster snapshots |
| FastCDC + BLAKE3 snapshots | Compare fixed chunks vs content-defined chunks on synthetic KB versions. | deduplication and integrity |
| Roaring / Elias-Fano postings | Build compact tag/source filters before vector search. | lower RAM for local RAG |
| SQLite FTS + vector sidecar | Hybrid lexical/vector retrieval on synthetic notes. | simple local search stack |
| SimHash / MinHash candidates | Preselect near-duplicates before deeper review. | cheaper dedup and clustering |
| Sparse projections | Test approximate similarity on sanitized embeddings. | lower-dimensional routing |
| Constrained JSON decoding | Require structured output for tool-facing steps. | safer automation boundaries |
| Semantic cache in shadow mode | Suggest reuse without automatic execution. | lower model spend with review |
| Small router model | Route easy tasks to cheap/local models and hard tasks to stronger models. | cost-aware QMeta execution |

## RU — связь с QMeta

QMeta может использовать эти методы как pre-processing and routing layer:

```text
raw task -> cheap filters -> candidate branches -> QMeta audit -> strong model only when needed -> traceable result
```

## EN — purpose

This module pack strengthens API/model credit applications: it shows that REDNET Airin/QMeta is designed not only to use strong models, but also to reduce context, memory, network, and compute cost.

## EN — principles

| Principle | Public experiment | Value |
|---|---|---|
| Zstd dictionaries for JSONL | Train small dictionaries on synthetic logs and compare size/latency. | cheaper storage and faster snapshots |
| FastCDC + BLAKE3 snapshots | Compare fixed chunks vs content-defined chunks on synthetic KB versions. | deduplication and integrity |
| Roaring / Elias-Fano postings | Build compact tag/source filters before vector search. | lower RAM for local RAG |
| SQLite FTS + vector sidecar | Hybrid lexical/vector retrieval on synthetic notes. | simple local search stack |
| SimHash / MinHash candidates | Preselect near-duplicates before deeper review. | cheaper dedup and clustering |
| Sparse projections | Test approximate similarity on sanitized embeddings. | lower-dimensional routing |
| Constrained JSON decoding | Require structured output for tool-facing steps. | safer automation boundaries |
| Semantic cache in shadow mode | Suggest reuse without automatic execution. | lower model spend with review |
| Small router model | Route easy tasks to cheap/local models and hard tasks to stronger models. | cost-aware QMeta execution |

## EN — QMeta integration

QMeta can use these methods as a pre-processing and routing layer:

```text
raw task -> cheap filters -> candidate branches -> QMeta audit -> strong model only when needed -> traceable result
```

## Public experiments

1. Synthetic JSONL compression benchmark.
2. Synthetic KB snapshot dedup benchmark.
3. Local hybrid search prototype with SQLite FTS.
4. Shadow-mode semantic cache with manual approval.
5. Cost-aware router report for QMeta branches.
