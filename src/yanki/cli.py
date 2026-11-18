"""Command-line entrypoint for Yankı verification and inference utilities."""

from __future__ import annotations

import argparse
import json
import sys

from .eval import main as eval_main
from .finetune import main as finetune_main
from .grounding import find_verbatim_span
from .guardrails import check_crisis_gate
from .providers import GroundedPipeline, HTTPInferenceBackend, ProviderConfig
from .train import main as train_main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="yanki", description="Yankı quote-grounding, alignment fine-tuning & safety CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_verify = sub.add_parser("verify", help="Verify a candidate quote against a source passage.")
    p_verify.add_argument("--source", required=True, help="Source passage text.")
    p_verify.add_argument("--quote", required=True, help="Candidate quote to verify.")

    p_gate = sub.add_parser("gate", help="Run the pre-inference safety gate on text.")
    p_gate.add_argument("--text", required=True, help="Input passage.")
    p_gate.add_argument("--lang", choices=["tr", "en"], default="tr")

    p_infer = sub.add_parser("reflect", help="Run safety-gated, quote-grounded reflection against an endpoint.")
    p_infer.add_argument("--text", required=True, help="Input journal passage (8..600 chars).")
    p_infer.add_argument("--lang", choices=["tr", "en"], default="tr")
    p_infer.add_argument("--provider", choices=["openai-compat", "anthropic"], default="openai-compat")
    p_infer.add_argument("--base-url", default=None)
    p_infer.add_argument("--model", default=None)

    sub.add_parser("eval", help="Delegate to yanki.eval benchmark runner (pass args after 'eval').")
    sub.add_parser("build-dataset", help="Build verified SFT & DPO preference JSONL files (yanki.finetune).")
    sub.add_parser("train", help="Launch or dry-run multi-GPU SFT/DPO alignment training (yanki.train).")

    raw_args = list(sys.argv[1:] if argv is None else argv)
    if raw_args and raw_args[0] == "eval":
        return eval_main(raw_args[1:])
    if raw_args and raw_args[0] == "build-dataset":
        return finetune_main(raw_args[1:])
    if raw_args and raw_args[0] == "train":
        return train_main(raw_args[1:])

    args = parser.parse_args(raw_args)

    if args.command == "verify":
        match = find_verbatim_span(args.source, args.quote)
        print(
            json.dumps(
                {
                    "grounded": match.grounded,
                    "start": match.start,
                    "end": match.end,
                    "exact_quote": match.exact_quote,
                    "lexical_overlap": match.lexical_overlap,
                    "reason": match.reason,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if match.grounded else 2

    if args.command == "gate":
        decision = check_crisis_gate(args.text, lang=args.lang)
        print(
            json.dumps(
                {
                    "triggered": decision.triggered,
                    "matched_pattern": decision.matched_pattern,
                    "response_text": decision.response_text,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.command == "reflect":
        base_cfg = ProviderConfig.from_env(args.provider)
        cfg = ProviderConfig(
            kind=base_cfg.kind,
            model=args.model or base_cfg.model,
            base_url=args.base_url or base_cfg.base_url,
            api_key=base_cfg.api_key,
        )
        pipeline = GroundedPipeline(HTTPInferenceBackend(cfg))
        result = pipeline.reflect(args.text, lang=args.lang)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
