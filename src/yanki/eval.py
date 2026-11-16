"""Offline and live-endpoint evaluation harness for quote-grounding and safety."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .grounding import find_verbatim_span, verify_cited_claims
from .guardrails import check_crisis_gate
from .providers import GroundedPipeline, HTTPInferenceBackend, ProviderConfig
from .schema import extract_json_object, validate_reflection

DEFAULT_SUITE = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "grounding_suite_tr_en.jsonl"


def load_suite(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue
            item = json.loads(stripped)
            item["_line"] = line_no
            cases.append(item)
    return cases


def run_offline_suite(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate deterministic verifier, schema contract, and crisis gate on ``cases``."""
    span_total = 0
    span_correct = 0
    hallucination_traps = 0
    hallucinations_caught = 0
    crisis_positives = 0
    crisis_tp = 0
    crisis_negatives = 0
    crisis_fp = 0
    schema_total = 0
    schema_correct = 0
    rag_total = 0
    rag_correct = 0
    failures: list[str] = []

    for case in cases:
        cid = case["id"]
        kind = case["kind"]

        if kind == "span":
            span_total += 1
            res = find_verbatim_span(case["source"], case.get("quote"))
            expected = bool(case["expect_grounded"])
            if res.grounded == expected:
                span_correct += 1
                if expected and "expect_exact" in case and res.exact_quote != case["expect_exact"]:
                    span_correct -= 1
                    failures.append(f"{cid}: expected slice {case['expect_exact']!r}, got {res.exact_quote!r}")
            else:
                failures.append(f"{cid}: expected grounded={expected}, got {res.grounded} ({res.reason})")

            if not expected:
                hallucination_traps += 1
                if not res.grounded:
                    hallucinations_caught += 1

        elif kind == "crisis":
            gate = check_crisis_gate(case["text"], lang=case.get("lang", "en"))
            expected = bool(case["expect_triggered"])
            if expected:
                crisis_positives += 1
                if gate.triggered:
                    crisis_tp += 1
                else:
                    failures.append(f"{cid}: missed crisis pattern in {case['text']!r}")
            else:
                crisis_negatives += 1
                if gate.triggered:
                    crisis_fp += 1
                    failures.append(f"{cid}: false positive ({gate.matched_pattern}) on {case['text']!r}")

        elif kind == "reflection_schema":
            schema_total += 1
            parsed = extract_json_object(case.get("raw_model_output"))
            validated = validate_reflection(parsed, case["source"])
            expect_valid = bool(case["expect_valid"])
            if expect_valid and validated is not None:
                if "expect_quote_stripped" in case and validated.quote_was_stripped != bool(case["expect_quote_stripped"]):
                    failures.append(f"{cid}: expected quote_was_stripped={case['expect_quote_stripped']}")
                else:
                    schema_correct += 1
            elif (not expect_valid) and validated is None:
                schema_correct += 1
            else:
                failures.append(f"{cid}: expected valid={expect_valid}, got {validated is not None}")

        elif kind == "multi_source_rag":
            rag_total += 1
            report = verify_cited_claims(case["sources"], case["claims"])
            if (
                report.grounded_claims == case["expect_grounded_count"]
                and report.dropped_claims == case["expect_dropped_count"]
            ):
                rag_correct += 1
            else:
                failures.append(
                    f"{cid}: expected grounded={case['expect_grounded_count']}/dropped={case['expect_dropped_count']}, "
                    f"got {report.grounded_claims}/{report.dropped_claims}"
                )

    return {
        "mode": "offline_deterministic",
        "total_cases": len(cases),
        "span_accuracy": round(span_correct / max(1, span_total), 4),
        "hallucination_rejection_rate": round(hallucinations_caught / max(1, hallucination_traps), 4),
        "crisis_recall": round(crisis_tp / max(1, crisis_positives), 4),
        "crisis_false_positive_rate": round(crisis_fp / max(1, crisis_negatives), 4),
        "schema_contract_accuracy": round(schema_correct / max(1, schema_total), 4),
        "multi_source_rag_accuracy": round(rag_correct / max(1, rag_total), 4),
        "failures": failures,
    }


def run_live_suite(
    cases: list[dict[str, Any]],
    config: ProviderConfig,
    limit: int | None = None,
) -> dict[str, Any]:
    """Run live end-to-end model inference + verification against an OpenAI/vLLM or Anthropic endpoint."""
    pipeline = GroundedPipeline(HTTPInferenceBackend(config))
    live_cases = [c for c in cases if c["kind"] in ("span", "crisis") and "source" in c or "text" in c]
    if limit is not None:
        live_cases = live_cases[:limit]

    valid_count = 0
    stripped_quotes = 0
    latencies: list[float] = []
    errors: list[str] = []

    for case in live_cases:
        passage = case.get("source") or case.get("text") or ""
        lang = case.get("lang", "tr" if any(ch in passage for ch in "ğüşıöçĞÜŞİÖÇ") else "en")
        try:
            res = pipeline.reflect(passage, lang=lang)
            valid_count += 1
            if res.get("quote_was_stripped"):
                stripped_quotes += 1
            if "latency_ms" in res:
                latencies.append(float(res["latency_ms"]))
        except Exception as exc:
            errors.append(f"{case['id']}: {exc}")

    lat_sorted = sorted(latencies)
    p50 = lat_sorted[len(lat_sorted) // 2] if lat_sorted else 0.0
    return {
        "mode": "live_endpoint",
        "provider": config.kind,
        "model": config.model,
        "base_url": config.base_url,
        "evaluated": len(live_cases),
        "valid_schema_rate": round(valid_count / max(1, len(live_cases)), 4),
        "ungrounded_quotes_stripped": stripped_quotes,
        "median_latency_ms": p50,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Yankı quote-grounding and safety benchmark runner.")
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE, help="Path to JSONL evaluation suite.")
    parser.add_argument("--offline", action="store_true", help="Run deterministic offline verification suite.")
    parser.add_argument("--provider", choices=["openai-compat", "anthropic"], default="openai-compat")
    parser.add_argument("--base-url", default=None, help="Override inference server base URL (e.g. vLLM http://127.0.0.1:8000/v1).")
    parser.add_argument("--model", default=None, help="Model identifier.")
    parser.add_argument("--limit", type=int, default=None, help="Limit live prompts evaluated.")
    parser.add_argument("--strict-thresholds", action="store_true", help="Exit non-zero if offline accuracy < 1.0.")
    parser.add_argument("--output", type=Path, default=None, help="Optional file path to write JSON metrics.")
    args = parser.parse_args(argv)

    cases = load_suite(args.suite)
    if args.offline or (args.base_url is None and args.model is None):
        report = run_offline_suite(cases)
    else:
        cfg = ProviderConfig.from_env(args.provider)
        cfg = ProviderConfig(
            kind=cfg.kind,
            model=args.model or cfg.model,
            base_url=args.base_url or cfg.base_url,
            api_key=cfg.api_key,
        )
        report = run_live_suite(cases, cfg, limit=args.limit)

    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    if args.strict_thresholds and report.get("failures"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
