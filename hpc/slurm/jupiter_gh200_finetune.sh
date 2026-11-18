#!/usr/bin/env bash
#SBATCH --job-name=yanki-gh200-dpo-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=4
#SBATCH --cpus-per-task=72
#SBATCH --time=08:00:00
#SBATCH --output=logs/jupiter_dpo_%j.out
#SBATCH --error=logs/jupiter_dpo_%j.err

# Multi-GPU distributed PyTorch (Stage 2026 PyTorch 2.9.1 / aarch64 Apptainer)
# SFT + DPO quote-grounding alignment fine-tuning recipe for JUPITER Booster
# (4x NVIDIA GH200 Grace Hopper Superchips per node, NVLink-C2C + NCCL).
#
# Container build prerequisite (run once with node-local APPTAINER_TMPDIR):
#   export APPTAINER_TMPDIR=${APPTAINER_TMPDIR:-/dev/shm}
#   apptainer build yanki_jupiter_aarch64.sif hpc/apptainer/yanki_jupiter_aarch64.def

set -euo pipefail

MODEL_ID="${MODEL_ID:-Qwen/Qwen2.5-32B-Instruct}"
DATA_DIR="${DATA_DIR:-artifacts/alignment_data}"
SFT_OUT="${SFT_OUT:-checkpoints/qwen32b_sft_${SLURM_JOB_ID:-local}}"
DPO_OUT="${DPO_OUT:-checkpoints/qwen32b_dpo_${SLURM_JOB_ID:-local}}"
SIF_IMAGE="${SIF_IMAGE:-yanki_jupiter_aarch64.sif}"
GPUS_PER_NODE="${GPUS_PER_NODE:-4}"

export OMP_NUM_THREADS=16
export NCCL_DEBUG=WARN

mkdir -p logs "${DATA_DIR}" checkpoints results

echo "[yanki-jupiter] Host architecture: $(uname -m) | Building verified TR/EN SFT + DPO datasets..."

if [[ -f "${SIF_IMAGE}" ]]; then
    RUNNER=(apptainer exec --nv "${SIF_IMAGE}")
else
    # Fallback to JSC Stage 2026 native software stack (PyTorch 2.9.1)
    module load Stages/2026 GCC PyTorch/2.9.1 2>/dev/null || true
    RUNNER=()
fi

"${RUNNER[@]}" python3 -m yanki.finetune --output-dir "${DATA_DIR}"

echo "[yanki-jupiter] Phase 1/3: Distributed FSDP LoRA SFT warmup on ${GPUS_PER_NODE}x GH200..."
"${RUNNER[@]}" torchrun \
    --standalone \
    --nproc_per_node="${GPUS_PER_NODE}" \
    -m yanki.train \
    --stage sft \
    --model "${MODEL_ID}" \
    --dataset "${DATA_DIR}/sft_train.jsonl" \
    --output-dir "${SFT_OUT}" \
    --epochs 1 \
    --lr 1e-5

echo "[yanki-jupiter] Phase 2/3: Distributed FSDP DPO quote-grounding preference alignment..."
"${RUNNER[@]}" torchrun \
    --standalone \
    --nproc_per_node="${GPUS_PER_NODE}" \
    -m yanki.train \
    --stage dpo \
    --model "${SFT_OUT}" \
    --dataset "${DATA_DIR}/dpo_preferences.jsonl" \
    --output-dir "${DPO_OUT}" \
    --dpo-beta 0.1 \
    --epochs 2 \
    --lr 5e-6

echo "[yanki-jupiter] Phase 3/3: Post-training deterministic grounding & crisis-gate verification..."
"${RUNNER[@]}" python3 -m yanki.eval \
    --offline \
    --strict-thresholds \
    --output "results/post_train_contract_${SLURM_JOB_ID:-local}.json"

echo "[yanki-jupiter] Fine-tuning completed: ${DPO_OUT}"
