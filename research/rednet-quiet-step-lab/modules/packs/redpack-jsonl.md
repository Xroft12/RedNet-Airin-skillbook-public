# Module: redpack-jsonl

## Identity

- Module ID: `redpack-jsonl`
- Type: `solution-pack`
- Status: `designed`
- Agent scope: `shared-readonly`
- Owner/reviewer: operator + Airin

## Purpose

Сжать повторяющиеся JSONL/KB/tool-trace корпуса через Zstd dictionaries без потери воспроизводимости.

## Discovery refs

- `#1 Zstd dictionaries for Hermes/KB JSONL`.
- Related: streaming sketches for telemetry.

## Inputs

- Sanitized JSONL corpora.
- Sample split for dictionary training.
- Baseline gzip/zstd/no-dict results.

## Outputs

- Dictionary file.
- Compression benchmark report.
- Restore/decode verification report.

## Safety boundaries

- Contains secrets: `false`; only sanitized samples.
- Requires network: `false`.
- Side effects: local files only.
- Allowed modes: `observe`, `shadow`, `soft`.
- Human approval required for: running over private/raw logs.

## Eval plan

- Baseline: raw, gzip, zstd no dictionary.
- Metrics:
  - compression ratio;
  - decode MB/s;
  - p95 object read latency;
  - exact restore SHA-256;
  - dictionary size.
- Pass gates:
  - byte-for-byte restore;
  - no secret-like strings in training sample;
  - decode latency acceptable for intended path.

## Promotion criteria

Reusable after at least 3 corpora show measurable savings and verified restores.
