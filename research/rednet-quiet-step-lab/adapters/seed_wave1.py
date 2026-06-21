#!/usr/bin/env python3
"""Seed Wave 1 RedNET Quiet Step Lab discoveries.

Safe/public contents only: no secrets, no raw private logs.
This script uses the local ingest adapter to create Markdown + JSONL + SQLite records.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ADAPTER = ROOT / "research" / "rednet-quiet-step-lab" / "adapters" / "subagent_ingest.py"

ENTRIES = [
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "pilot_now",
        "title": "Zstd dictionaries for Hermes/KB JSONL",
        "tags": "compression,zstd,jsonl,hermes",
        "evidence": "RFC 8878 Zstandard; https://github.com/facebook/zstd; https://github.com/Cyan4973/FiniteStateEntropy",
        "text": "Principle: Zstd + FSE/Huff0 with trained dictionaries for repetitive small objects. Buys disk/bandwidth/latency for JSONL logs, KB chunks and snapshots. Breaks on already compressed/encrypted heterogeneous data; high levels can spike CPU; whole-file compression hurts random access. RedNET experiment: train per-corpus dictionaries for Hermes logs, RAG chunks and tool traces; compare raw/gzip/zstd/no-dict/dict by ratio, decode MB/s and p95 object latency.",
    },
    {
        "role": "compression-hunter",
        "kind": "architecture",
        "status": "pilot_now",
        "title": "FastCDC + BLAKE3 content-addressed snapshots",
        "tags": "cdc,cas,blake3,nas,backup",
        "evidence": "FastCDC USENIX ATC 2016; https://github.com/google/cdc-file-transfer; https://github.com/BLAKE3-team/BLAKE3",
        "text": "Principle: content-defined chunking makes versions resilient to byte insertions; BLAKE3 hashes address chunks. Buys NAS sync time, dedup, integrity and incremental restore. Breaks on encrypted/compressed inputs; chunk size and metadata need tuning; CAS needs GC. RedNET experiment: compare fixed-size chunks vs FastCDC on KB/log snapshots, measure unique bytes, metadata, restore SHA-256 and rebuild time.",
    },
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "pilot_now",
        "title": "Roaring + Elias-Fano postings for compact local RAG filters",
        "tags": "roaring,elias-fano,postings,rag,index",
        "evidence": "https://github.com/RoaringBitmap/CRoaring; Roaring bitmaps papers; Vigna Elias-Fano/quasi-succinct indices",
        "text": "Principle: mutable/hot docsets use Roaring containers; cold sorted postings use Elias-Fano. Buys RAM and fast AND/OR filtering before vector/FTS retrieval. Breaks on high-churn updates or tiny lists where overhead dominates. RedNET experiment: export term/tag/source postings from KB and compare SQLite joins vs Roaring/EF blobs on size, p95 latency and exact docset equality.",
    },
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "pilot_now",
        "title": "FST/MARISA trie for command and term dictionaries",
        "tags": "fst,marisa,trie,commands,lexicon",
        "evidence": "https://github.com/s-yata/marisa-trie; https://github.com/BurntSushi/fst",
        "text": "Principle: sorted strings compile to minimal automata and can be mmap-read compactly. Buys startup/RAM/prefix lookup speed for command aliases, term dictionaries and prompt/template names. Breaks because updates require rebuild and Unicode normalization must be strict. RedNET experiment: build a static dictionary of commands/tags/terms; compare JSON/SQLite vs MARISA/FST by file size, RSS and lookup latency.",
    },
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "pilot_now",
        "title": "Xor/Binary Fuse filters before SQLite/NAS shard lookup",
        "tags": "xor-filter,binary-fuse,probabilistic,index",
        "evidence": "https://github.com/FastFilter/xor_singleheader; Xor Filters papers by Graf/Lemire",
        "text": "Principle: static fingerprint filters answer membership queries with tiny bytes/key and controlled false positives. Buys fewer disk/NAS/SQLite probes for shards and CAS blocks. Breaks on dynamic sets and adversarial keys; false positives require exact verifier. RedNET experiment: build filters over chunk hashes and term IDs; compare Bloom vs Xor/Binary Fuse for bytes/key, FPR, build time and lookup latency.",
    },
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "audit_first",
        "title": "Minimal Perfect Hash for immutable RedNET cold indexes",
        "tags": "mph,recsplit,pthash,bbhash,index",
        "evidence": "RecSplit arXiv:1910.06416; https://github.com/jermp/pthash; https://github.com/rizkg/BBHash",
        "text": "Principle: immutable key set maps to dense collision-free IDs, payload stored in arrays. Buys RAM and lookup speed for hash->offset, term->id, command->handler_id. Breaks on updates; unknown-key guard is required because MPH alone is not membership. RedNET experiment: use Xor filter + MPH for chunk_hash->location and compare against SQLite primary key and Python dict.",
    },
    {
        "role": "compression-hunter",
        "kind": "algorithm",
        "status": "pilot_now",
        "title": "Streaming sketches for low-privacy telemetry",
        "tags": "hll,count-min,datasketches,telemetry",
        "evidence": "Apache DataSketches; Count-Min Sketch; HyperLogLog; t-digest",
        "text": "Principle: keep compact approximate summaries for cardinality, heavy hitters and quantiles instead of raw event streams. Buys fixed-memory telemetry and safer compact dashboards. Breaks when exact audit counts are required; collisions and adversarial streams need salted hashes. RedNET experiment: replay safe logs and compare sketches vs exact SQL group-by on memory, time and error.",
    },
    {
        "role": "compression-hunter",
        "kind": "source",
        "status": "scout",
        "title": "Procedural/demoscene compression as prompt-template grammar",
        "tags": "procedural,demoscene,templates,grammar",
        "evidence": "farbrausch .kkrieger; demoscene 4k/64k intro tooling",
        "text": "Principle: store seed + grammar + deterministic renderer instead of repeated assets/templates. Buys tokens, storage and maintainability for repeated help/status/prompt boilerplate. Breaks on authoring complexity and sandbox/security for code generators. RedNET experiment: replace repeated Telegram/help/prompt templates with macro DSL and measure bytes/tokens and readability.",
    },
    {
        "role": "compression-hunter",
        "kind": "risk",
        "status": "red_zone",
        "title": "Context mixing compressors only as cold oracle",
        "tags": "context-mixing,zpaq,cmix,cold-archive",
        "evidence": "ZPAQ; cmix; Large Text Compression Benchmark",
        "text": "Principle: many statistical context models maximize lossless compression ratio. Buys offline upper-bound estimates for compressibility. Breaks badly in runtime due to CPU/RAM/random-access cost. RedNET rule: never put context mixing in Hermes interactive path; use only cold benchmark lane against zstd --long/dict.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "pilot_now",
        "title": "LSH/SimHash/MinHash candidate cascades",
        "tags": "lsh,simhash,minhash,candidate,retrieval",
        "evidence": "Indyk-Motwani LSH; Charikar SimHash; Broder MinHash",
        "text": "Principle: similar items collide with higher probability, e.g. random hyperplane SimHash P[same sign]=1-theta/pi. Buys sublinear candidate retrieval for memory, duplicate detection and cache matching. Breaks if bands/hash count are mis-tuned or adversarial collisions occur. RedNET experiment: LSH proposes candidates, exact semantic/rule verifier decides; compare recall@50 and wall-clock against brute force.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "pilot_now",
        "title": "Sparse Johnson-Lindenstrauss projections",
        "tags": "jl,random-projection,dimensionality,retrieval",
        "evidence": "Johnson-Lindenstrauss lemma; Achlioptas database-friendly random projections",
        "text": "Principle: m=O(log n / epsilon^2) random dimensions approximately preserve pairwise distances. Buys cheap compressed embeddings and prefiltering. Breaks if semantic metric is not Euclidean or rare distinctions collapse. RedNET experiment: project context vectors to 64/128/256 dims, exact-rerank shortlist and measure recall@K, distortion, latency and RAM.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "pilot_now",
        "title": "HDC/VSA hypervector associative memory",
        "tags": "hdc,vsa,hrr,associative-memory",
        "evidence": "Kanerva hyperdimensional computing; Plate holographic reduced representations; vector symbolic architectures",
        "text": "Principle: high-dimensional random vectors bind/bundle role-filler structures; similarity recovers candidates under noise. Buys CPU-cheap approximate symbolic recall and one-shot traces. Breaks by crosstalk/capacity limits; cannot be final factual authority. RedNET experiment: encode task/tool/outcome/constraint traces and compare recall candidates against JSON and embedding memory.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "pilot_now",
        "title": "Kalman/Bayesian belief state for agent runs",
        "tags": "kalman,bayesian,state,trust,budget",
        "evidence": "Kalman 1960; Bayesian filtering; extended/particle filters",
        "text": "Principle: predict/update loop tracks hidden state and uncertainty from noisy observations. Buys calibrated confidence over tool reliability, cost, failure probability and need for human check. Breaks with wrong noise model or regime shifts. RedNET experiment: replay past runs and predict escalation/failure; evaluate Brier score/AUC vs moving average.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "pilot_now",
        "title": "Randomized low-rank SVD/Nystrom for retrieval structure",
        "tags": "low-rank,svd,nystrom,matrix",
        "evidence": "Halko-Martinsson-Tropp randomized SVD arXiv:0909.4061; Williams-Seeger Nystrom",
        "text": "Principle: A≈QQ^T A via random range finder; kernels approximated by C W† C^T. Buys compressed retrieval matrices and faster clustering/rerank. Breaks when spectrum is not low-rank or rare safety modes are discarded. RedNET experiment: approximate embedding similarity at ranks 16/32/64 and measure recall, outlier miss rate and latency.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "audit_first",
        "title": "Compressed sensing for sparse diagnostic probes",
        "tags": "compressed-sensing,sparse,diagnostics",
        "evidence": "Candes-Romberg-Tao compressed sensing; Donoho compressed sensing; Baraniuk survey",
        "text": "Principle: k-sparse causes can be recovered from m<<n measurements via l1 minimization under assumptions. Buys fewer diagnostic probes when failures are sparse. Breaks if causes are correlated/non-sparse or measurement matrix is bad. RedNET experiment: inject synthetic sparse failures and compare recovered causes vs exhaustive ablation.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "audit_first",
        "title": "Information Bottleneck / MDL summaries",
        "tags": "information-bottleneck,mdl,summary,context",
        "evidence": "Tishby-Pereira-Bialek information bottleneck; Rissanen MDL",
        "text": "Principle: compress X into Z while preserving task-relevant Y; MDL minimizes model+data description length. Buys principled context compression and anti-bloat memory. Breaks because MI estimates are hard and rare safety constraints may vanish. RedNET experiment: compare naive vs obligation-preserving summaries on downstream accuracy and safety-fact retention.",
    },
    {
        "role": "math-hunter",
        "kind": "formula",
        "status": "scout",
        "title": "Tensor Train/MPS factorized routing state",
        "tags": "tensor-train,mps,policy,routing",
        "evidence": "Oseledets Tensor-Train Decomposition; Matrix Product States reviews",
        "text": "Principle: high-order tensor T[i1..id]=G1[i1]...Gd[id] compresses interactions to O(d n r^2). Buys compression of task/tool/risk/budget policy tables. Breaks if rank explodes or dimension ordering is bad. RedNET experiment: learn a factorized routing tensor from traces and compare dense/CP/Tucker/TT under equal memory.",
    },
    {
        "role": "math-hunter",
        "kind": "source",
        "status": "scout",
        "title": "Quantum-inspired length-square candidate sampling",
        "tags": "quantum-inspired,length-square,sampling,candidates",
        "evidence": "Tang arXiv:1807.04271 quantum-inspired recommendation; Frieze-Kannan-Vempala length-square sampling",
        "text": "Principle: sample rows/columns by squared norm to build low-rank or recommendation candidates. Buys candidate selection when low-rank/norm structure exists. Breaks if preprocessing dominates; no quantum speedup on classical hardware. RedNET experiment: use as classical heuristic, then exact rerank; explicitly label quantum-inspired, not quantum acceleration.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "prototype",
        "status": "pilot_now",
        "title": "llama.cpp GGUF quantization matrix",
        "tags": "llama.cpp,gguf,quantization,nano-llm",
        "evidence": "https://github.com/ggml-org/llama.cpp; ggml GGUF docs",
        "text": "Principle: run local GGUF quantizations Q8/Q5_K_M/Q4_K_M and measure quality-speed-memory tradeoff. Buys CPU/local inference and RAM savings for nano assistants. Breaks on rare terminology, JSON/tool robustness and long context. RedNET experiment: fixed benchmark of Russian/scientific/tool prompts with tok/s, RAM, JSON pass and answer pass.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "prototype",
        "status": "audit_first",
        "title": "Speculative decoding with draft verifier split",
        "tags": "speculative-decoding,latency,draft,verifier",
        "evidence": "arXiv:2211.17192; arXiv:2302.01318",
        "text": "Principle: small draft proposes tokens, larger model verifies accepted prefix. Buys latency for long free-form answers. Breaks if acceptance rate is low, tokenizers differ, or constrained JSON is active. RedNET experiment: enable only for long free-form prompts; measure acceptance rate, p50/p95 latency and semantic diff.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "architecture",
        "status": "pilot_now",
        "title": "Semantic cache in shadow mode",
        "tags": "semantic-cache,shadow,cache,telemetry",
        "evidence": "https://github.com/zilliztech/GPTCache",
        "text": "Principle: compute similarity and potential hits but do not serve cached answers until precision is proven. Buys safe estimate of cache savings and repeated-question clusters. Breaks on stale answers, tenant leakage, false semantic matches and embedding drift. RedNET experiment: namespace per project, log intent/hash/answer signature, review 100 nearest-neighbor pairs.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "architecture",
        "status": "pilot_now",
        "title": "ONNX/sklearn risk and cost router",
        "tags": "onnx,sklearn,router,risk,cost",
        "evidence": "ONNX Runtime traditional ML; scikit-learn calibration",
        "text": "Principle: calibrated lightweight classifier routes request to cache/small/large/human/block. Buys deterministic cheap gating and lower latency/cost. Breaks under dataset shift or false negatives on high-risk tasks. RedNET experiment: shadow mode with features for PII/cyber/code/schema/cache/source-count; evaluate AUROC/ECE/confusion matrix and ONNX p95 latency.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "architecture",
        "status": "pilot_now",
        "title": "sqlite-vec + BM25 hybrid local RAG",
        "tags": "sqlite-vec,bm25,rag,hybrid,local",
        "evidence": "https://github.com/asg017/sqlite-vec; SQLite FTS5",
        "text": "Principle: combine FTS5/BM25 exact search with vector kNN and reciprocal rank fusion. Buys single-file local RAG, reproducibility and citations with low ops. Breaks on very large corpora, write concurrency and poor embeddings. RedNET experiment: 200 docs/50 queries, compare BM25 vs vector vs hybrid on recall@5, MRR and hallucination rate.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "prototype",
        "status": "pilot_now",
        "title": "Constrained decoding / JSON schema for tool safety",
        "tags": "constrained-decoding,json-schema,tools,safety",
        "evidence": "https://github.com/noamgat/lm-format-enforcer; https://github.com/dottxt-ai/outlines",
        "text": "Principle: grammar/JSON Schema restricts valid tokens at decode time. Buys parse-pass rate, fewer retries and safer tool args. Breaks because syntax validity is not semantic validity and strict schemas can slow/overconstrain. RedNET experiment: 100 prompts freeform+repair vs constrained; measure parse pass, schema validity and latency.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "risk",
        "status": "audit_first",
        "title": "KV cache quantization / eviction",
        "tags": "kv-cache,quantization,context,memory",
        "evidence": "LLM KV cache quantization papers including arXiv:2405.04434; llama.cpp KV discussions",
        "text": "Principle: store K/V activations at lower precision or evict/compress old context. Buys longer context and more sessions per RAM/VRAM. Breaks on long-range reasoning, exact citations and implementation regressions. RedNET experiment: canary only; never evict citations/definitions; compare FP16/Q8/Q4 KV on long scientific QA with citation exactness.",
    },
    {
        "role": "ai-nano-hunter",
        "kind": "risk",
        "status": "audit_first",
        "title": "DSPy and QLoRA only behind frozen eval",
        "tags": "dspy,qlora,peft,eval,safety",
        "evidence": "https://github.com/stanfordnlp/dspy; QLoRA arXiv:2305.14314; https://github.com/artidoro/qlora",
        "text": "Principle: DSPy optimizes prompt/RAG programs; QLoRA trains adapters over 4-bit base models. Buys task-specific quality without full fine-tune. Breaks by overfit, data leakage, license contamination and safety regression. RedNET experiment: DSPy-first on frozen train/dev/test; QLoRA only after dataset/license/safety audit.",
    },
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def main() -> int:
    init = run([sys.executable, str(ADAPTER), "init"])
    if init.returncode != 0:
        print(init.stdout)
        print(init.stderr, file=sys.stderr)
        return init.returncode

    inserted = []
    failed = []
    for entry in ENTRIES:
        cmd = [
            sys.executable,
            str(ADAPTER),
            "ingest",
            "--role", entry["role"],
            "--kind", entry["kind"],
            "--status", entry["status"],
            "--title", entry["title"],
            "--tags", entry["tags"],
            "--evidence", entry["evidence"],
            "--source", "wave1-subagents-2026-06-09",
            "--text", entry["text"],
        ]
        result = run(cmd)
        if result.returncode == 0:
            inserted.append({"status": entry["status"], "title": entry["title"], "stdout": result.stdout.strip()})
        else:
            failed.append({"title": entry["title"], "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})

    export = run([sys.executable, str(ADAPTER), "export-council"])
    listing = run([sys.executable, str(ADAPTER), "list", "--limit", "80"])

    print(json.dumps({
        "entries_total": len(ENTRIES),
        "inserted_count": len(inserted),
        "failed_count": len(failed),
        "failed": failed,
        "export_returncode": export.returncode,
        "export_stdout": export.stdout.strip(),
        "export_stderr": export.stderr.strip(),
        "list_returncode": listing.returncode,
        "list_stdout": listing.stdout,
    }, ensure_ascii=False, indent=2))
    return 0 if not failed and export.returncode == 0 and listing.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
