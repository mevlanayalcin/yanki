# Yankı — Multilingual Quote-Grounding & Deterministic LLM Verification Engine

[![CI](https://github.com/mevlanayalcin/yanki/actions/workflows/ci.yml/badge.svg)](https://github.com/mevlanayalcin/yanki/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Yankı** is an open-source bilingual (`TR` / `EN`) LLM verification, pre-inference safety gating, and verbatim quote-grounding engine, accompanied by its live zero-retention Cloudflare Worker deployment ([mevlanayalcin.com.tr/work/yanki](https://mevlanayalcin.com.tr/work/yanki/)).

Rather than trusting language models to self-police safety boundaries or quote source documents faithfully, Yankı enforces deterministic pre- and post-inference invariants in code:

1. **Turkish-Aware Offset-Preserving Normalization (`yanki.normalize`):** Standard Unicode lowercasing turns Turkish `İ` (`U+0130`) into a 2-codepoint sequence (`i\u0307`), corrupting character offsets when slicing back into UTF-8 texts. `build_normalized_view()` folds Turkish/Latin diacritics (`ğ, ü, ş, ı, İ, ö, ç`) while maintaining exact character provenance maps `[start, end)` into the original document.
2. **Deterministic Verbatim Quote & Multi-Source Citation Verification (`yanki.grounding`):** Every quoted span emitted by an LLM (both single-passage reflections and multi-document RAG synthesis claims) is checked against the raw source text. Paraphrased or fabricated quotes are deterministically stripped or rejected, and verified spans are re-sliced directly from the original source characters.
3. **Pre-Inference Lexical Safety Gate (`yanki.guardrails`):** High-risk crisis expressions in Turkish and English are intercepted *before* any model API or GPU server is called.
4. **Zero-Fallback Schema Contracts & Multi-Provider Routing (`yanki.schema`, `yanki.providers`):** Supports local/cluster **OpenAI-compatible GPU servers (`vLLM`, `SGLang`, `NVIDIA NIM`, `Fireworks`)** alongside the **Anthropic Messages API** using Python's standard library HTTP stack (zero mandatory SDK bloat inside HPC containers). Malformed model outputs fail closed instead of emitting synthetic fallback prose.

---

## Repository Layout

| Path | Description |
|---|---|
| `src/yanki/` | Core Python package: Turkish-aware offset normalizer, span/citation verifier, safety gate, schema contracts, `vLLM`/OpenAI/Anthropic client, CLI & benchmark runner |
| `benchmarks/grounding_suite_tr_en.jsonl` | Bilingual (`TR` / `EN`) deterministic evaluation suite covering Turkish `İ/ı` offsets, paraphrase traps, multi-source RAG claims, and safety boundaries |
| `hpc/apptainer/yanki_vllm_cuda.def` | Apptainer (`--nv`) container recipe (`PyTorch 24.09 + vLLM`) for GPU supercomputing clusters |
| `hpc/slurm/berzelius_vllm_eval.sh` | Slurm batch job launching node-local tensor-parallel `vLLM` inference + `yanki.eval` |
| `tests/test_yanki_engine.py` | Unit & integration test suite (including parity checks against `data/ornekler.json`) |
| `cloudflare/worker.mjs` | Production Cloudflare Worker serving `/api/reflect`, `/api/waitlist`, and `/api/health` with Durable Object rate limiting |
| `scripts/` & `site/` | Static bilingual product/documentation generator and live deployment health auditor (`denet.py`) |

---

## Quickstart (Python Engine & Evaluation Suite)

```bash
python3 -m pip install -e ".[dev]"

# Run unit and parity tests
pytest -v

# Run the deterministic offline quote-grounding & safety benchmark
python3 -m yanki.eval --offline --strict-thresholds

# Verify a Turkish quote span from the CLI (recovers original UTF-8 slice & offsets)
yanki verify \
  --source "İstanbul'dan Ankara'ya döndüğümden beri hiçbir işe odaklanamıyorum." \
  --quote "istanbul'dan ankara'ya dondugumden beri"
```

### Evaluating Open-Weight Models on `vLLM` / `SGLang` (CUDA / Slurm HPC)

Point `yanki.eval` at any OpenAI-compatible GPU server (`Qwen2.5-32B/72B`, `Llama-3.3-70B`, `DeepSeek-R1-Distill`, `Mistral`):

```bash
python3 -m yanki.eval \
  --provider openai-compat \
  --base-url http://127.0.0.1:8000/v1 \
  --model Qwen/Qwen2.5-32B-Instruct \
  --output results/qwen32b_eval.json
```

For multi-GPU Slurm clusters with Apptainer (`A100` / `H100` / `H200`), build the container and submit the batch job in `hpc/`:

```bash
apptainer build yanki_vllm_cuda.sif hpc/apptainer/yanki_vllm_cuda.def
MODEL_ID="Qwen/Qwen2.5-32B-Instruct" TP_SIZE=4 sbatch hpc/slurm/berzelius_vllm_eval.sh
```

### Python API Example

```python
from yanki import find_verbatim_span, verify_cited_claims

# 1. Single-source Turkish diacritic-insensitive span verification
match = find_verbatim_span(
    "Sunum sırasında göğsüm sıkıştı ama sonuna kadar devam ettim.",
    "gogsum sikisti ama sonuna kadar",
)
assert match.grounded is True
print(match.start, match.end, match.exact_quote)
# -> 16 47 "göğsüm sıkıştı ama sonuna kadar"

# 2. Multi-source primary document citation verification
report = verify_cited_claims(
    sources={"doc_1": "Tensor parallelism across four H200 GPUs reduced p95 latency to 118 ms."},
    claims=[
        {"claim": "4x H200 cut p95 latency to 118 ms.", "source_id": "doc_1", "quote": "reduced p95 latency to 118 ms"},
        {"claim": "Paraphrased claim", "source_id": "doc_1", "quote": "cut tail latency down to 118ms"},
    ],
)
print(report.grounded_claims, report.dropped_claims)  # -> 1, 1
```

---

## Edge Deployment (Cloudflare Worker + Static Assets)

The live web beta at [mevlanayalcin.com.tr/work/yanki/](https://mevlanayalcin.com.tr/work/yanki/) runs `cloudflare/worker.mjs` with zero journal-text persistence (only aggregate daily token-unit counters and opt-in waitlist entries in KV, plus per-IP rate limiting via Durable Objects):

```bash
python3 scripts/build.py
npx --yes wrangler@4.148.0 dev --local --port 4173 --host localhost --local-upstream localhost

# Production deploy & end-to-end live check
npx --yes wrangler@4.148.0 deploy --dry-run --keep-vars
npx --yes wrangler@4.148.0 deploy --keep-vars
python3 scripts/denet.py https://mevlanayalcin.com.tr
```

### Scope & Explicit Boundaries (Türkçe Özet)

- **Deterministik Alıntı Doğrulaması:** Modelin ürettiği `alinti` / `quote` alanı kaynak metinde birebir (Türkçe karakter ve büyük/küçük harf duyarsız normalizasyon sonrası bitişik alt dizge olarak) yer almıyorsa otomatik olarak ayıklanır; model kaynakta olmayan bir cümleyi alıntı gibi gösteremez.
- **Ön-Çıkarım Güvenlik Kapısı:** Kriz ifadeleri modele gitmeden önce deterministik kural katmanında yakalanır. Yankı terapi, teşhis veya tıbbi hizmet değildir.
- **Sıfır Sahte Yedek Cevap:** Şema doğrulamasından geçemeyen bozuk model çıktılarında kural tabanlı uydurma cevap üretilmez.

---

## License

Released under the [MIT License](LICENSE). Maintained by Mevlana Yalçın (`info@mevlanayalcin.com.tr`).
