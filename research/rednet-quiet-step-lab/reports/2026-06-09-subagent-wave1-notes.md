# Wave 1 subagent notes

Дата: 2026-06-09.

## Запущенные роли

### 1. Архивариус компактности

Статус: completed.

Добыча:

- Zstd dictionaries + FSE/Huff0.
- FastCDC/Gear chunking + BLAKE3 CAS.
- Roaring + Elias-Fano postings.
- FST/MARISA lexicon.
- Xor/Binary Fuse filters.
- Minimal Perfect Hash.
- Streaming sketches.
- FSST/columnar compression.
- FM-index/wavelet tree.
- Product Quantization for RAG embeddings.
- Procedural/demoscene grammar.
- Context mixing as cold oracle.

### 2. Математик тонких рычагов

Статус: completed.

Добыча:

- Sparse JL random projections.
- LSH/SimHash/MinHash cascades.
- Streaming sketches.
- HDC/VSA/HRR hypervector memory.
- Kalman/Bayesian filters.
- Randomized low-rank SVD/Nystrom.
- Wavelets.
- Compressed sensing.
- Information Bottleneck / MDL.
- Reservoir computing.
- Tensor Train / MPS.
- Quantum-inspired length-square sampling.

### 3. AI/nano-LLM systems engineer

Статус: first attempt timeout; short retry completed.

Причина: первая попытка застряла на медленных web/API fetch циклах и была остановлена по timeout. Результат не был засчитан как завершённый. Затем был запущен короткий ограниченный повтор.

Добыча короткого повтора:

- llama.cpp/GGUF quantization matrix.
- Speculative decoding.
- Semantic cache shadow.
- ONNX/sklearn risk router.
- sqlite-vec + BM25 hybrid RAG.
- Constrained decoding / JSON schema.
- KV cache quantization/eviction.
- DSPy/QLoRA behind frozen eval.

## Что загружено в ledger

- Всего карточек: 26.
- compression-hunter: 9.
- math-hunter: 9.
- ai-nano-hunter: 8.
- pilot_now: 16.
- audit_first: 6.
- scout: 3.
- red_zone: 1.

## Примечание о проверке

Два саба использовали web evidence handles; AI/nano повтор проверял только быстро и часть источников помечена как handles, требующие дальнейшей формальной допроверки перед внедрением.
