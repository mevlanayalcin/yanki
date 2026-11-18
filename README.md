# Yankı — Multilingual Quote-Grounding Alignment Fine-Tuning (SFT/DPO) & Deterministic LLM Verification Engine

[![CI](https://github.com/mevlanayalcin/yanki/actions/workflows/ci.yml/badge.svg)](https://github.com/mevlanayalcin/yanki/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Yankı** is an open-source bilingual (`TR` / `EN`) post-training alignment pipeline (**distributed multi-GPU PyTorch FSDP LoRA SFT + DPO preference fine-tuning**), pre-inference safety gate, and verbatim quote-grounding verification engine, accompanied by its zero-retention edge deployment ([mevlanayalcin.com.tr/work/yanki](https://mevlanayalcin.com.tr/work/yanki/)).

Open-weight multilingual language models (`Qwen2.5-32B/72B`, `Llama-3.3-70B`, `DeepSeek-R1-Distill`, `Mistral`) frequently paraphrase, reorder words, or corrupt Turkish UTF-8 character spans (`İ` / `ı`) when asked to cite primary sources verbatim. Yankı combines **preference post-training on HPC GPU clusters** with **deterministic runtime verification**:

1. **Hard-Negative SFT & DPO Alignment Dataset Synthesis (`yanki.finetune`):** Automatically constructs supervised fine-tuning (`messages`) trajectories and Direct Preference Optimization (`prompt`, `chosen`, `rejected`) preference pairs where `chosen` carries character-verified UTF-8 spans and `rejected` injects realistic Turkish/English near-miss paraphrases, word-order swaps, and ungrounded citations.
2. **Multi-GPU Distributed PyTorch FSDP LoRA + DPO Post-Training (`yanki.train`):** Native `torchrun` (`NCCL` / `RCCL`, `bfloat16`, `FSDP`, `PEFT LoRA`) SFT warmup and reference-free DPO fine-tuning loop built for EuroHPC supercomputers — including **JUPITER Booster (`NVIDIA GH200` `aarch64`, `Stage 2026 PyTorch 2.9.1`)**, **LUMI-G (`AMD Instinct MI250X` `ROCm`)**, and **`H100` / `H200` / `GB200`** clusters.
3. **Turkish-Aware Offset-Preserving Normalization (`yanki.normalize`):** Standard Unicode lowercasing turns Turkish `İ` (`U+0130`) into a 2-codepoint sequence (`i\u0307`), corrupting character offsets when slicing back into UTF-8 texts. `build_normalized_view()` folds Turkish/Latin diacritics (`ğ, ü, ş, ı, İ, ö, ç`) while maintaining exact character provenance maps `[start, end)` into the original document.
4. **Deterministic Verbatim Quote & Multi-Source Citation Verification (`yanki.grounding`, `yanki.guardrails`, `yanki.schema`):** Pre-inference lexical crisis gating intercepts high-risk `TR`/`EN` expressions before model execution, and post-inference verification deterministically strips any paraphrased or fabricated quote span.

---

## Repository Layout

| Path | Description |
|---|---|
| `src/yanki/finetune.py` | Verified SFT & hard-negative DPO preference dataset builder (`sft_train.jsonl`, `dpo_preferences.jsonl`) |
| `src/yanki/train.py` | Multi-GPU `torchrun` PyTorch (`FSDP` + `LoRA`, `bf16`) SFT & DPO post-training alignment runner |
| `src/yanki/{normalize,grounding,guardrails,schema,providers,eval}.py` | Core Turkish-aware offset normalizer, span/citation verifier, safety gate, schema contracts, and post-training evaluator |
| `hpc/apptainer/yanki_jupiter_aarch64.def` | `aarch64` (`linux/arm64`) Apptainer training container recipe for **JUPITER Booster (`GH200`)** (`APPTAINER_TMPDIR=/dev/shm`) |
| `hpc/slurm/jupiter_gh200_finetune.sh` | Slurm `4x GH200` (`aarch64` / `Stage 2026 PyTorch 2.9.1`) distributed SFT + DPO fine-tuning & post-training validation job |
| `hpc/slurm/lumi_rocm_finetune.sh` | Slurm `8x GCD` (`AMD Instinct MI250X` ROCm) distributed DPO fine-tuning job for **EuroHPC LUMI-G** |
| `hpc/apptainer/yanki_vllm_cuda.def` & `hpc/slurm/berzelius_vllm_eval.sh` | Post-training `vLLM` checkpoint evaluation container and Slurm job for `x86_64` CUDA clusters |
| `benchmarks/grounding_suite_tr_en.jsonl` | Bilingual (`TR` / `EN`) deterministic evaluation suite covering Turkish `İ/ı` offsets, paraphrase traps, multi-source RAG claims, and safety boundaries |
| `tests/test_yanki_engine.py` | Unit & integration test suite covering SFT/DPO pair synthesis, DPO loss math, dry-run trainer validation, and grounding parity |
| `cloudflare/worker.mjs` | Production Cloudflare Worker serving `/api/reflect`, `/api/waitlist`, and `/api/health` with Durable Object rate limiting |

---

## Quickstart (Alignment Dataset, Fine-Tuning & Evaluation)

```bash
python3 -m pip install -e ".[dev]"

# 1. Run unit, SFT/DPO dataset, and parity tests
pytest -v

# 2. Build verified bilingual SFT & hard-negative DPO preference JSONL datasets
python3 -m yanki.finetune --output-dir artifacts/alignment_data

# 3. Validate DPO training configuration & preference invariants (CPU dry-run)
python3 -m yanki.train \
  --stage dpo \
  --model Qwen/Qwen2.5-32B-Instruct \
  --dataset artifacts/alignment_data/dpo_preferences.jsonl \
  --dry-run

# 4. Run the deterministic offline quote-grounding & safety benchmark
python3 -m yanki.eval --offline --strict-thresholds
```

### Multi-GPU SFT + DPO Fine-Tuning on EuroHPC (`JUPITER GH200 aarch64` & `LUMI-G`)

On **JUPITER Booster (`NVIDIA GH200`, `aarch64`)**, build the ARM64 Apptainer image using node-local `/dev/shm` (never shared GPFS storage) or load `Stages/2026 PyTorch/2.9.1`, then submit the distributed `FSDP` LoRA SFT + DPO job:

```bash
export APPTAINER_TMPDIR=${APPTAINER_TMPDIR:-/dev/shm}
apptainer build yanki_jupiter_aarch64.sif hpc/apptainer/yanki_jupiter_aarch64.def

MODEL_ID="Qwen/Qwen2.5-32B-Instruct" sbatch hpc/slurm/jupiter_gh200_finetune.sh
```

On **EuroHPC LUMI-G (`AMD Instinct MI250X`, ROCm)**:

```bash
MODEL_ID="Qwen/Qwen2.5-32B-Instruct" sbatch hpc/slurm/lumi_rocm_finetune.sh
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
