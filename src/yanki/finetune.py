"""SFT and DPO preference-pair dataset builder and verifier for quote-grounding alignment.

Constructs supervised fine-tuning (SFT) conversations and Direct Preference Optimization
(DPO / SimPO) hard-negative preference pairs ``(prompt, chosen, rejected)`` where:
  * ``chosen`` satisfies strict JSON schema validation and 100% verbatim character-span
    grounding (preserving Turkish ``İ/ı`` UTF-8 offsets), and
  * ``rejected`` contains realistic near-miss paraphrase, word-order, or fabricated-span
    corruptions that fail ``find_verbatim_span``.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from .grounding import find_verbatim_span, verify_cited_claims
from .guardrails import check_crisis_gate
from .schema import extract_json_object, validate_grounded_synthesis, validate_reflection

SYSTEM_PROMPT_TR = (
    "Sen Yankı alıntı-doğrulamalı yansıtma modelisin. Yalnızca geçerli JSON üret. "
    "'alinti' alanı kaynak metinde geçen birebir bitişik alt dizge olmak zorundadır; "
    "asla yeniden ifade etme veya kelimeleri değiştirme."
)

SYSTEM_PROMPT_EN = (
    "You are the Yanki quote-grounded synthesis and reflection model. Emit strict JSON only. "
    "Every 'alinti' or 'quote' span must be a contiguous verbatim substring of the source passage; "
    "never paraphrase, reorder tokens, or invent quotations."
)

_TR_PARAPHRASE_SWAPS: tuple[tuple[str, str], ...] = (
    ("gereksiz", "değersiz"),
    ("odaklanamıyorum", "konsantre olamıyorum"),
    ("sıkışma", "baskı"),
    ("uykusuz", "yorgun"),
    ("titredi", "sarsıldı"),
    ("bırakmış", "azaltmış"),
    ("yine", "tekrar"),
    ("hiçbir", "artık hiçbir"),
)

_EN_PARAPHRASE_SWAPS: tuple[tuple[str, str], ...] = (
    ("tight", "heavy and tight"),
    ("flat", "completely numb"),
    ("drained", "exhausted"),
    ("reduced", "cut down"),
    ("avoiding", "putting off"),
    ("cancelled", "postponed"),
    ("exhausted", "worn out"),
)


@dataclass(frozen=True)
class SFTExample:
    """Supervised fine-tuning chat trajectory with verified character-offset provenance."""

    id: str
    lang: str
    messages: list[dict[str, str]]
    source_text: str
    exact_quote: str
    start: int
    end: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PreferenceExample:
    """DPO preference pair contrasting a verbatim-grounded completion with a paraphrase trap."""

    id: str
    lang: str
    prompt: list[dict[str, str]]
    source_text: str
    chosen: str
    rejected: str
    exact_quote: str
    rejected_quote: str
    rejection_reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def corrupt_verbatim_quote(exact_quote: str, source_text: str, lang: str = "tr") -> str:
    """Synthesize a hard-negative near-miss paraphrase of ``exact_quote`` not verbatim in ``source_text``."""
    swaps = _TR_PARAPHRASE_SWAPS if lang == "tr" else _EN_PARAPHRASE_SWAPS
    lowered = exact_quote.lower()
    for target, replacement in swaps:
        idx = lowered.find(target)
        if idx >= 0:
            candidate = exact_quote[:idx] + replacement + exact_quote[idx + len(target) :]
            if not find_verbatim_span(source_text, candidate).grounded:
                return candidate

    words = exact_quote.split()
    if len(words) >= 3:
        reordered = " ".join([words[0], words[-1], *words[1:-1]])
        if not find_verbatim_span(source_text, reordered).grounded:
            return reordered

    suffix = " tamamen" if lang == "tr" else " completely"
    fallback = f"{exact_quote}{suffix}"
    if not find_verbatim_span(source_text, fallback).grounded:
        return fallback
    return "uydurulmus kaynak disi alinti" if lang == "tr" else "fabricated non-source quotation"


def verify_preference_pair(pair: PreferenceExample) -> tuple[bool, str]:
    """Verify DPO invariant: ``chosen`` grounds verbatim while ``rejected`` fails grounding."""
    chosen_obj = extract_json_object(pair.chosen)
    rejected_obj = extract_json_object(pair.rejected)
    if chosen_obj is None or rejected_obj is None:
        return False, "invalid_json_envelope"

    if "claims" in chosen_obj:
        sources = {"doc_0": pair.source_text}
        c_res = validate_grounded_synthesis(chosen_obj, sources, require_all_grounded=True)
        r_res = validate_grounded_synthesis(rejected_obj, sources, require_all_grounded=True)
        if c_res is None or c_res.grounded_claims == 0:
            return False, "chosen_synthesis_ungrounded"
        if r_res is not None:
            return False, "rejected_synthesis_unexpectedly_grounded"
        return True, "verified_synthesis_dpo_pair"

    c_ref = validate_reflection(chosen_obj, pair.source_text)
    r_ref = validate_reflection(rejected_obj, pair.source_text)
    if c_ref is None or c_ref.alinti is None or c_ref.quote_was_stripped:
        return False, "chosen_reflection_ungrounded"
    if r_ref is None or not r_ref.quote_was_stripped:
        return False, "rejected_reflection_not_stripped"
    return True, "verified_reflection_dpo_pair"


def _make_reflection_json(lang: str, quote: str) -> str:
    if lang == "tr":
        payload = {
            "duygu": "gerginlik",
            "siddet": 3,
            "alternatif": "yorgunluk",
            "yansitma": "Paylaştığın ifadede belirgin bir yük ve zihinsel yorgunluk hissediliyor.",
            "alinti": quote,
            "adim": "Ekran başından kısa süreliğine ayrılıp nefesini sakinleştir.",
        }
    else:
        payload = {
            "duygu": "strain",
            "siddet": 3,
            "alternatif": "fatigue",
            "yansitma": "Your passage captures a clear sense of accumulated pressure and mental fatigue.",
            "alinti": quote,
            "adim": "Step away from your workspace for ten quiet minutes.",
        }
    return json.dumps(payload, ensure_ascii=False)


def build_alignment_examples(
    suite_cases: list[dict[str, Any]],
    ornekler: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[list[SFTExample], list[PreferenceExample]]:
    """Construct verified SFT and DPO examples from benchmark suites and bilingual corpora."""
    sft_rows: list[SFTExample] = []
    dpo_rows: list[PreferenceExample] = []

    for case in suite_cases:
        kind = case.get("kind")
        cid = str(case.get("id") or f"case-{len(sft_rows)}")
        if kind == "span" and case.get("expect_grounded"):
            source = str(case["source"])
            lang = str(case.get("lang") or ("tr" if any(c in source for c in "ğüşıöçĞÜŞİÖÇ") else "en"))
            if check_crisis_gate(source, lang=lang).triggered:
                continue
            span = find_verbatim_span(source, str(case["quote"]))
            if not span.grounded or span.exact_quote is None or span.start is None or span.end is None:
                continue

            sys_prompt = SYSTEM_PROMPT_TR if lang == "tr" else SYSTEM_PROMPT_EN
            chosen_json = _make_reflection_json(lang, span.exact_quote)
            bad_quote = corrupt_verbatim_quote(span.exact_quote, source, lang=lang)
            rejected_json = _make_reflection_json(lang, bad_quote)
            bad_span = find_verbatim_span(source, bad_quote)

            prompt_msgs = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": source},
            ]
            sft_rows.append(
                SFTExample(
                    id=f"sft-{cid}",
                    lang=lang,
                    messages=[*prompt_msgs, {"role": "assistant", "content": chosen_json}],
                    source_text=source,
                    exact_quote=span.exact_quote,
                    start=span.start,
                    end=span.end,
                )
            )
            pair = PreferenceExample(
                id=f"dpo-{cid}",
                lang=lang,
                prompt=prompt_msgs,
                source_text=source,
                chosen=chosen_json,
                rejected=rejected_json,
                exact_quote=span.exact_quote,
                rejected_quote=bad_quote,
                rejection_reason=bad_span.reason,
            )
            ok, _ = verify_preference_pair(pair)
            if ok:
                dpo_rows.append(pair)

        elif kind == "multi_source_rag":
            sources: dict[str, str] = dict(case.get("sources") or {})
            report = verify_cited_claims(sources, list(case.get("claims") or []))
            for idx, vclaim in enumerate(report.verified):
                if vclaim.exact_quote is None or vclaim.start is None or vclaim.end is None:
                    continue
                src_text = sources[vclaim.source_id]
                lang = "tr" if any(c in src_text for c in "ğüşıöçĞÜŞİÖÇ") else "en"
                bad_q = corrupt_verbatim_quote(vclaim.exact_quote, src_text, lang=lang)
                chosen_syn = json.dumps(
                    {
                        "summary": vclaim.claim,
                        "claims": [{"claim": vclaim.claim, "source_id": "doc_0", "quote": vclaim.exact_quote}],
                    },
                    ensure_ascii=False,
                )
                rejected_syn = json.dumps(
                    {
                        "summary": vclaim.claim,
                        "claims": [{"claim": vclaim.claim, "source_id": "doc_0", "quote": bad_q}],
                    },
                    ensure_ascii=False,
                )
                prompt_msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT_TR if lang == "tr" else SYSTEM_PROMPT_EN},
                    {"role": "user", "content": f"[doc_0] {src_text}"},
                ]
                sft_rows.append(
                    SFTExample(
                        id=f"sft-{cid}-{idx}",
                        lang=lang,
                        messages=[*prompt_msgs, {"role": "assistant", "content": chosen_syn}],
                        source_text=src_text,
                        exact_quote=vclaim.exact_quote,
                        start=vclaim.start,
                        end=vclaim.end,
                    )
                )
                pair = PreferenceExample(
                    id=f"dpo-{cid}-{idx}",
                    lang=lang,
                    prompt=prompt_msgs,
                    source_text=src_text,
                    chosen=chosen_syn,
                    rejected=rejected_syn,
                    exact_quote=vclaim.exact_quote,
                    rejected_quote=bad_q,
                    rejection_reason=find_verbatim_span(src_text, bad_q).reason,
                )
                ok, _ = verify_preference_pair(pair)
                if ok:
                    dpo_rows.append(pair)

    if ornekler:
        for lang in ("tr", "en"):
            for idx, item in enumerate(ornekler.get(lang, [])):
                if item.get("kriz"):
                    continue
                source = str(item.get("girdi") or "")
                raw_q = item.get("alıntı") or item.get("alinti")
                if not source or not raw_q:
                    continue
                span = find_verbatim_span(source, str(raw_q))
                if not span.grounded or span.exact_quote is None or span.start is None or span.end is None:
                    continue
                chosen_payload = {
                    "duygu": item.get("duygu") or ("yorgunluk" if lang == "tr" else "fatigue"),
                    "siddet": int(item.get("şiddet") or item.get("siddet") or 3),
                    "alternatif": item.get("alternatif"),
                    "yansitma": item.get("yansıtma") or item.get("yansitma") or _make_reflection_json(lang, span.exact_quote),
                    "alinti": span.exact_quote,
                    "adim": item.get("adım") or item.get("adim"),
                }
                if validate_reflection(chosen_payload, source) is None:
                    continue
                bad_q = corrupt_verbatim_quote(span.exact_quote, source, lang=lang)
                rejected_payload = {**chosen_payload, "alinti": bad_q}
                chosen_str = json.dumps(chosen_payload, ensure_ascii=False)
                rejected_str = json.dumps(rejected_payload, ensure_ascii=False)
                prompt_msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT_TR if lang == "tr" else SYSTEM_PROMPT_EN},
                    {"role": "user", "content": source},
                ]
                sft_rows.append(
                    SFTExample(
                        id=f"sft-ornek-{lang}-{idx}",
                        lang=lang,
                        messages=[*prompt_msgs, {"role": "assistant", "content": chosen_str}],
                        source_text=source,
                        exact_quote=span.exact_quote,
                        start=span.start,
                        end=span.end,
                    )
                )
                pair = PreferenceExample(
                    id=f"dpo-ornek-{lang}-{idx}",
                    lang=lang,
                    prompt=prompt_msgs,
                    source_text=source,
                    chosen=chosen_str,
                    rejected=rejected_str,
                    exact_quote=span.exact_quote,
                    rejected_quote=bad_q,
                    rejection_reason=find_verbatim_span(source, bad_q).reason,
                )
                ok, _ = verify_preference_pair(pair)
                if ok:
                    dpo_rows.append(pair)

    return sft_rows, dpo_rows


def export_alignment_jsonl(
    output_dir: Path,
    suite_path: Path | None = None,
    ornekler_path: Path | None = None,
) -> dict[str, Any]:
    """Export ``sft_train.jsonl`` and ``dpo_preferences.jsonl`` into ``output_dir``."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    resolved_suite = suite_path or (repo_root / "benchmarks" / "grounding_suite_tr_en.jsonl")
    resolved_ornekler = ornekler_path if ornekler_path is not None else (repo_root / "data" / "ornekler.json")

    suite_cases: list[dict[str, Any]] = []
    with resolved_suite.open("r", encoding="utf-8") as handle:
        for raw in handle:
            stripped = raw.strip()
            if stripped and not stripped.startswith("#"):
                suite_cases.append(json.loads(stripped))

    ornekler_data: dict[str, list[dict[str, Any]]] | None = None
    if resolved_ornekler.exists():
        ornekler_data = json.loads(resolved_ornekler.read_text(encoding="utf-8"))

    sft_rows, dpo_rows = build_alignment_examples(suite_cases, ornekler=ornekler_data)
    output_dir.mkdir(parents=True, exist_ok=True)
    sft_file = output_dir / "sft_train.jsonl"
    dpo_file = output_dir / "dpo_preferences.jsonl"

    sft_file.write_text(
        "\n".join(json.dumps(r.to_dict(), ensure_ascii=False) for r in sft_rows) + ("\n" if sft_rows else ""),
        encoding="utf-8",
    )
    dpo_file.write_text(
        "\n".join(json.dumps(r.to_dict(), ensure_ascii=False) for r in dpo_rows) + ("\n" if dpo_rows else ""),
        encoding="utf-8",
    )

    return {
        "sft_count": len(sft_rows),
        "dpo_count": len(dpo_rows),
        "sft_path": str(sft_file),
        "dpo_path": str(dpo_file),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build verified SFT & DPO quote-grounding training datasets.")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/alignment_data"))
    parser.add_argument("--suite", type=Path, default=None)
    parser.add_argument("--ornekler", type=Path, default=None)
    args = parser.parse_args(argv)

    summary = export_alignment_jsonl(
        output_dir=args.output_dir,
        suite_path=args.suite,
        ornekler_path=args.ornekler,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["sft_count"] > 0 and summary["dpo_count"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
