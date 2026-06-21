# Module: hybrid-local-rag

## Identity

- Module ID: `hybrid-local-rag`
- Type: `solution-pack`
- Status: `designed`
- Agent scope: `airin / shared-readonly`
- Owner/reviewer: operator + Airin

## Purpose

Локальный RAG-позвоночник лаборатории: SQLite FTS5/BM25 + vector kNN + reciprocal rank fusion + citations.

## Discovery refs

- `#23 sqlite-vec + BM25 hybrid local RAG`.
- Related: Roaring/Elias-Fano filters, JL projections, HDC recall.

## Inputs

- Public/sanitized docs.
- Chunk manifests.
- Query/eval set.
- Embedding model selected under free/local constraints.

## Outputs

- SQLite DB.
- Retrieval report.
- Citation-grounded answer candidates.

## Safety boundaries

- Contains secrets: `false` by default.
- Requires network: `false` after dependencies/model are present.
- Side effects: local index files only.
- Allowed modes: `observe`, `shadow`.
- Human approval required for: indexing private work/medical data, external sync, answer-serving.

## Eval plan

- Baseline: BM25 only and vector only.
- Metrics:
  - Recall@5;
  - MRR;
  - citation exactness;
  - hallucination rate;
  - build time and DB size.
- Pass gates:
  - answers must cite retrieved chunks;
  - no citation, no factual claim;
  - private corpora require separate namespace and approval.

## Promotion criteria

Reusable after 50-query frozen eval beats BM25/vector baselines without citation regression.
