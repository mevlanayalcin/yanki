#!/usr/bin/env bash
#SBATCH --job-name=yanki-grounding-eval
#SBATCH --gpus=4
#SBATCH --cpus-per-gpu=8
#SBATCH --mem=128G
#SBATCH --time=02:00:00
#SBATCH --output=logs/yanki_eval_%j.out
#SBATCH --error=logs/yanki_eval_%j.err

# Offline single-node vLLM + Yankı quote-grounding evaluation recipe for Slurm
# NVIDIA clusters (e.g. NAISS Berzelius A100/H200, HLRS, or standard CUDA nodes).

set -euo pipefail

MODEL_ID="${MODEL_ID:-Qwen/Qwen2.5-32B-Instruct}"
TP_SIZE="${TP_SIZE:-4}"
PORT="${PORT:-18000}"
SIF_IMAGE="${SIF_IMAGE:-yanki_vllm_cuda.sif}"
OUT_JSON="${OUT_JSON:-results/eval_${SLURM_JOB_ID:-local}.json}"

mkdir -p logs results

echo "[yanki-hpc] Starting local vLLM server for ${MODEL_ID} (TP=${TP_SIZE}) on 127.0.0.1:${PORT}"

apptainer exec --nv "${SIF_IMAGE}" \
    python3 -m vllm.entrypoints.openai.api_server \
    --host 127.0.0.1 \
    --port "${PORT}" \
    --model "${MODEL_ID}" \
    --tensor-parallel-size "${TP_SIZE}" \
    --max-model-len 8192 \
    --dtype bfloat16 &
VLLM_PID=$!

cleanup() {
    if kill -0 "${VLLM_PID}" 2>/dev/null; then
        kill "${VLLM_PID}" || true
        wait "${VLLM_PID}" 2>/dev/null || true
    fi
}
trap cleanup EXIT

for _ in $(seq 1 90); do
    if curl -sf "http://127.0.0.1:${PORT}/v1/models" >/dev/null 2>&1; then
        echo "[yanki-hpc] vLLM server ready."
        break
    fi
    sleep 5
done

apptainer exec --nv "${SIF_IMAGE}" \
    python3 -m yanki.eval \
    --provider openai-compat \
    --base-url "http://127.0.0.1:${PORT}/v1" \
    --model "${MODEL_ID}" \
    --output "${OUT_JSON}"

echo "[yanki-hpc] Evaluation written to ${OUT_JSON}"
