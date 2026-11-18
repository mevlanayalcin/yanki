"""Multi-GPU distributed PyTorch (FSDP / DDP + LoRA) SFT & DPO fine-tuning runner.

Designed for EuroHPC supercomputing environments including:
  * JUPITER Booster (NVIDIA GH200 Grace Hopper ``aarch64``, Stage 2026 PyTorch 2.9.1, NCCL)
  * LUMI-G (AMD Instinct MI250X, ROCm / RCCL)
  * NVIDIA H100 / H200 / GB200 Slurm clusters via ``torchrun``

Supports ``--dry-run`` dataset and configuration verification without requiring ``torch``
to be installed on lightweight CI hosts.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import os
from pathlib import Path
from typing import Any

from .finetune import PreferenceExample, verify_preference_pair


@dataclass(frozen=True)
class TrainingConfig:
    """Hyperparameters and distributed runtime settings for SFT / DPO post-training."""

    stage: str = "dpo"  # "sft" or "dpo"
    model_name_or_path: str = "Qwen/Qwen2.5-32B-Instruct"
    dataset_path: str = "artifacts/alignment_data/dpo_preferences.jsonl"
    output_dir: str = "checkpoints/yanki-qwen32b-grounding-dpo"
    max_seq_len: int = 4096
    per_device_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 5e-6
    dpo_beta: float = 0.1
    lora_rank: int = 64
    lora_alpha: int = 128
    lora_dropout: float = 0.05
    epochs: int = 2
    bf16: bool = True
    fsdp: bool = True

    def validate(self) -> None:
        if self.stage not in ("sft", "dpo"):
            raise ValueError(f"Unsupported stage: {self.stage!r} (expected 'sft' or 'dpo')")
        if self.max_seq_len < 128:
            raise ValueError("max_seq_len must be >= 128")
        if self.per_device_batch_size < 1 or self.gradient_accumulation_steps < 1:
            raise ValueError("batch size and gradient_accumulation_steps must be >= 1")
        if self.dpo_beta <= 0.0:
            raise ValueError("dpo_beta must be > 0")
        if self.lora_rank < 4:
            raise ValueError("lora_rank must be >= 4")


def compute_reference_free_dpo_loss_scalar(
    chosen_avg_logp: float,
    rejected_avg_logp: float,
    beta: float = 0.1,
) -> float:
    """Reference-free DPO (SimPO-style) scalar logistic preference loss ``-log sigmoid(beta * margin)``."""
    margin = beta * (chosen_avg_logp - rejected_avg_logp)
    if margin >= 0:
        return math.log1p(math.exp(-margin))
    return -margin + math.log1p(math.exp(margin))


def load_jsonl_records(path: Path, stage: str) -> list[dict[str, Any]]:
    """Load and structurally validate SFT or DPO training JSONL records."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            stripped = raw.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            if stage == "sft":
                if not isinstance(item.get("messages"), list) or len(item["messages"]) < 2:
                    raise ValueError(f"Line {line_no}: SFT record requires 'messages' list")
            else:
                pair = PreferenceExample(
                    id=str(item.get("id") or f"line-{line_no}"),
                    lang=str(item.get("lang") or "tr"),
                    prompt=list(item["prompt"]),
                    source_text=str(item["source_text"]),
                    chosen=str(item["chosen"]),
                    rejected=str(item["rejected"]),
                    exact_quote=str(item.get("exact_quote") or ""),
                    rejected_quote=str(item.get("rejected_quote") or ""),
                    rejection_reason=str(item.get("rejection_reason") or "paraphrased_not_verbatim"),
                )
                ok, reason = verify_preference_pair(pair)
                if not ok:
                    raise ValueError(f"Line {line_no} ({pair.id}) failed DPO verification: {reason}")
            records.append(item)

    if not records:
        raise ValueError(f"Dataset {path} contains 0 valid records")
    return records


def _run_pytorch_distributed_training(cfg: TrainingConfig, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute distributed PyTorch LoRA SFT / DPO training loop under ``torchrun``."""
    import torch
    import torch.distributed as dist
    import torch.nn.functional as F
    from transformers import AutoModelForCausalLM, AutoTokenizer

    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    distributed = world_size > 1

    if distributed and not dist.is_initialized():
        backend = "nccl" if torch.cuda.is_available() else "gloo"
        dist.init_process_group(backend=backend)

    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_device(device)

    dtype = torch.bfloat16 if (cfg.bf16 and torch.cuda.is_available()) else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name_or_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name_or_path,
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    model.gradient_checkpointing_enable()

    try:
        from peft import LoraConfig, get_peft_model

        lora_cfg = LoraConfig(
            r=cfg.lora_rank,
            lora_alpha=cfg.lora_alpha,
            lora_dropout=cfg.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        )
        model = get_peft_model(model, lora_cfg)
    except ImportError:
        pass

    model.to(device)
    if distributed and cfg.fsdp and torch.cuda.is_available():
        from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

        model = FSDP(model, device_id=local_rank, use_orig_params=True)
    elif distributed:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[local_rank] if torch.cuda.is_available() else None)

    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=cfg.learning_rate,
        weight_decay=0.01,
    )

    def _seq_logprob(messages: list[dict[str, str]]) -> torch.Tensor:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        enc = tokenizer(
            text,
            truncation=True,
            max_length=cfg.max_seq_len,
            return_tensors="pt",
        ).to(device)
        out = model(**enc)
        shift_logits = out.logits[:, :-1, :].contiguous()
        shift_labels = enc["input_ids"][:, 1:].contiguous()
        log_probs = F.log_softmax(shift_logits, dim=-1)
        token_lp = log_probs.gather(-1, shift_labels.unsqueeze(-1)).squeeze(-1)
        return token_lp.mean()

    model.train()
    rank = dist.get_rank() if (distributed and dist.is_initialized()) else 0
    sharded = records[rank::world_size]
    total_steps = 0
    losses: list[float] = []

    optimizer.zero_grad()
    for _epoch in range(cfg.epochs):
        for step_idx, row in enumerate(sharded, 1):
            if cfg.stage == "sft":
                lp = _seq_logprob(row["messages"])
                loss = -lp / cfg.gradient_accumulation_steps
            else:
                chosen_msgs = [*row["prompt"], {"role": "assistant", "content": row["chosen"]}]
                rejected_msgs = [*row["prompt"], {"role": "assistant", "content": row["rejected"]}]
                c_lp = _seq_logprob(chosen_msgs)
                r_lp = _seq_logprob(rejected_msgs)
                loss = -F.logsigmoid(cfg.dpo_beta * (c_lp - r_lp)) / cfg.gradient_accumulation_steps

            loss.backward()
            losses.append(float(loss.detach().cpu().item()) * cfg.gradient_accumulation_steps)

            if step_idx % cfg.gradient_accumulation_steps == 0 or step_idx == len(sharded):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                optimizer.zero_grad()
                total_steps += 1

    out_path = Path(cfg.output_dir)
    if rank == 0:
        out_path.mkdir(parents=True, exist_ok=True)
        target_model = model.module if hasattr(model, "module") else model
        target_model.save_pretrained(out_path)
        tokenizer.save_pretrained(out_path)

    if distributed and dist.is_initialized():
        dist.barrier()
        dist.destroy_process_group()

    return {
        "mode": "pytorch_distributed",
        "stage": cfg.stage,
        "model": cfg.model_name_or_path,
        "world_size": world_size,
        "records": len(records),
        "optimizer_steps": total_steps,
        "mean_loss": round(sum(losses) / max(1, len(losses)), 6),
        "output_dir": str(out_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Yankı distributed SFT & DPO alignment trainer.")
    parser.add_argument("--stage", choices=["sft", "dpo"], default="dpo")
    parser.add_argument("--model", default="Qwen/Qwen2.5-32B-Instruct")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("checkpoints/yanki-grounding-dpo"))
    parser.add_argument("--max-seq-len", type=int, default=4096)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=5e-6)
    parser.add_argument("--dpo-beta", type=float, default=0.1)
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--no-fsdp", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate dataset & training config without GPU execution.")
    args = parser.parse_args(argv)

    cfg = TrainingConfig(
        stage=args.stage,
        model_name_or_path=args.model,
        dataset_path=str(args.dataset),
        output_dir=str(args.output_dir),
        max_seq_len=args.max_seq_len,
        per_device_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        dpo_beta=args.dpo_beta,
        lora_rank=args.lora_rank,
        epochs=args.epochs,
        fsdp=not args.no_fsdp,
    )
    cfg.validate()
    records = load_jsonl_records(args.dataset, stage=cfg.stage)

    if args.dry_run:
        summary = {
            "mode": "dry_run_validated",
            "config": asdict(cfg),
            "verified_records": len(records),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    report = _run_pytorch_distributed_training(cfg, records)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
