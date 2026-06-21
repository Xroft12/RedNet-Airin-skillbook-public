# RedNET Quiet Step Lab — Wave 1 Digest

Дата: 2026-06-09.  
Режим: сабагентская охота + Совет/двойная оценка, без платных API и без изменений инфраструктуры.

## 0. Главный вывод первой волны

Мы на правильной линии: **не догонять GPU-гонку объёмом**, а строить каскад, где дешёвые структуры уменьшают пространство поиска, а дорогая модель включается только там, где она нужна.

Сжатые и вероятностные методы не становятся “истиной”. Они становятся охотничьими собаками:

```text
sketch / filter / cache / projection
  -> candidates
  -> exact verifier
  -> small model
  -> larger model or human only if needed
```

## 1. Добыча группы компактности

### Pilot now

1. **Zstd dictionaries / FSE / ANS**
   - Evidence: `https://github.com/facebook/zstd`, `https://github.com/Cyan4973/FiniteStateEntropy`, `https://arxiv.org/abs/1311.2540`.
   - Что покупает: плотное и быстрое сжатие JSONL/log/KB, особенно с обученным словарём.
   - RedNET: отдельные словари для Hermes logs, tool traces, KB chunks, sensor JSONL.

2. **Content-defined chunking / FastCDC / CAS**
   - Evidence: USENIX FastCDC, `https://github.com/restic/chunker`.
   - Что покупает: версии KB/logs не копируются целиком; вставка байта не ломает дедуп.
   - RedNET: NAS-first snapshots + SQLite manifest + zstd chunks.

3. **FST/MARISA + Elias-Fano/Roaring postings**
   - Evidence: MARISA, CRoaring, Elias-Fano papers.
   - Что покупает: компактный и быстрый локальный индекс для KB/RAG.
   - RedNET: prefilter перед embeddings/LLM.

4. **Xor/Binary Fuse filters + Minimal Perfect Hashing**
   - Evidence: FastFilter/xor_singleheader, PTHash/BBHash repos.
   - Что покупает: быстрый ответ “есть ли ключ в shard?” без disk seek.
   - RedNET: shard gate для KB, sensor IDs, command registry.

5. **Sketch summaries: HLL / Count-Min / DataSketches**
   - Evidence: HLL++ Google paper, Count-Min Sketch, Apache DataSketches.
   - Что покупает: статистика потока без хранения raw потока.
   - RedNET: privacy-preserving telemetry на Ubuntu edge.

### Scout / research

- Demoscene procedural assets: `.kkrieger`, Crinkler, Shader Minifier — принцип “asset = seed + grammar + renderer”.
- CMIX/ZPAQ/context mixing — не runtime, а offline oracle для выявления полезных контекстов.

## 2. Математическая добыча

### Формулы-рычаги

1. **Compressed sensing**: `y = Φx`, `m = O(k log(n/k))`, восстановление `min ||x||₁`.
2. **Johnson–Lindenstrauss**: `m = O(ε⁻² log N)` сохраняет расстояния.
3. **Count-Min Sketch**: `w≈e/ε`, `d≈ln(1/δ)`, ошибка `≤ ε||a||₁`.
4. **Low-rank SVD/Nyström**: `A ≈ UₖΣₖVₖᵀ`, `K ≈ C W† Cᵀ`.
5. **Tensor Train/MPS**: `T[i₁…i_d] = G₁[i₁]…G_d[i_d]`, параметры `O(d n r²)`.
6. **SRHT/RFF**: `y = √(n/m) R H D x`, `φ(x)ᵀφ(y) ≈ k(x,y)`.
7. **Wavelets**: `x = Σ c_{j,k} ψ_{j,k}`, thresholding coefficients.
8. **HDC/VSA/HRR**: bind `a ⊗ b`, bundle `sign(Σvᵢ)`.
9. **Bloom filters**: `p≈(1-e^{-kn/m})^k`, `k≈(m/n)ln2`.
10. **Kalman/Bayesian belief state**: `K=P⁻Hᵀ(HP⁻Hᵀ+R)⁻¹`.
11. **Reservoir computing**: `h_t=tanh(W_in x_t + W h_{t-1})`, обучается `W_out`.
12. **Information Bottleneck / MDL**: `min I(X;T)-βI(T;Y)`, `min L(model)+L(data|model)`.

### Важное ограничение

Quantum-inspired идеи полезны как матрицы поиска и амплификации кандидатов, но не дают квантового ускорения на CPU без quantum oracle/hardware. Не выдавать метафору за физику.

## 3. AI / nano-LLM добыча

### Pilot now

1. **GGUF/llama.cpp local inference matrix** — сравнить Q4/Q5/Q8 на frozen eval prompts.
2. **Speculative decoding** — draft ускоряет, но не принимает решений.
3. **Semantic cache shadow mode** — сначала кэш только пишет потенциальный hit, не отвечает.
4. **ONNX/sklearn nano-router** — классифицирует cache/small/large/human/risk.
5. **sqlite-vec local RAG** — векторы и provenance рядом с ledger, без отдельной vector DB.

### Audit first

- KV-cache quantization/eviction: риск потери критичных токенов.
- DSPy optimizer: хорош только при хорошей метрике.
- QLoRA/adapters: только на очищенных размеченных наборах, не self-training.

## 4. Десять связок, которые выглядят прорывными для нас

1. Zstd dictionary + JSONL normalized keys + SQLite blob manifest.
2. CDC-CAS + zstd + NAS mirror + restore-to-staging.
3. FST dictionary + Elias-Fano sparse postings + Roaring dense sets.
4. Xor filter + MPH + compressed shard blocks.
5. HDC/VSA event memory + LSH cleanup + exact ledger verifier.
6. JL random projection + LSH similar incident search + exact rules.
7. Wavelet anomaly detector + Bayesian/Kalman health state.
8. Reservoir sequence classifier + ONNX export + Guardian escalation.
9. Semantic cache shadow + router regret ledger + small-first model cascade.
10. sqlite-vec/BM25 hybrid RAG + context compression only for background chunks.

## 5. Что применяем уже сейчас

- Создана структура лаборатории `research/rednet-quiet-step-lab/`.
- Создан адаптер `adapters/subagent_ingest.py`.
- Создан backlog первых экспериментов.
- Создан единый слой карточек: Markdown + JSONL + SQLite.
- Первая партия карточек загружается адаптером в ledger.

## 6. Лучший кандидат на постоянную научную роль

Пока лидирует роль:

**RedNET Quiet PI — Cascade/Eval Architect**

Метрики отличия:

- small-first resolution rate;
- quality delta against frozen baseline;
- latency/power per successful task;
- cache precision;
- escalation precision/recall;
- reproducibility через SQLite ledger;
- умение сказать “не знаю, нужен verifier”.

## 7. Риски

- Low-rank может выбросить редкий критичный хвост.
- Probabilistic filters могут стать ложной правдой без exact verify.
- Semantic cache может протащить устаревший или приватный ответ.
- Context compression может удалить маленькую критичную деталь.
- Self-training на собственных ответах может закрепить галлюцинации.

## 8. Следующая волна

- Проверка URL/handles для математических источников.
- Реальный micro-benchmark `redpack-jsonl`.
- Реальный CDC-CAS staging restore.
- HDC/VSA prototype на synthetic event cases.
- Shadow semantic cache на безопасном наборе повторяющихся задач.
