#!/usr/bin/env bash
#SBATCH --job-name=yanki-lumi-dpo-train
#SBATCH --partition=standard-g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=8
#SBATCH --cpus-per-task=56
#SBATCH --mem=480G
#SBATCH --time=06:00:00
#SBATCH --output=logs/lumi_dpo_%j.out
#SBATCH --error=logs/lumi_dpo_%j.err

# Multi-GCD distributed ROCm / PyTorch FSDP LoRA SFT + DPO fine-tuning recipe
# for EuroHPC LUMI-G (4x AMD Instinct MI250X = 8 GCDs per node).

set -euo pipefail

MODEL_ID="${MODEL_ID:-Qwen/Qwen2.5-32B-Instruct}"
DATA_DIR="${DATA_DIR:-artifacts/alignment_data}"
OUT_DIR="${OUT_DIR:-checkpoints/lumi_qwen32b_dpo_${SLURM_JOB_ID:-local}}"

module use /appl/local/csc/modulefiles 2>/dev/null || true
module load pytorch 2>/dev/null || true

mkdir -p logs "${DATA_DIR}" checkpoints

python3 -m yanki.finetune --output-dir "${DATA_DIR}"

torchrun \
    --standalone \
    --nproc_per_node=8 \
    -m yanki.train \
    --stage dpo \
    --model "${MODEL_ID}" \
    --dataset "${DATA_DIR}/dpo_preferences.jsonl" \
    --output-dir "${OUT_DIR}" \
    --dpo-beta 0.1 \
    --epochs 2 \
    --lr 5e-6
