"""Strict JSON envelope extraction and zero-fallback schema validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from typing import Any

from .grounding import CitationReport, verify_cited_claims, verify_quote_grounding

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", flags=re.IGNORECASE | re.DOTALL)
_FENCE_START_RE = re.compile(r"^\s*```(?:json)?\s*", flags=re.IGNORECASE)
_FENCE_END_RE = re.compile(r"\s*```\s*$")


@dataclass(frozen=True)
class ReflectionResult:
    """Validated structured output for bilingual reflection prompts."""

    duygu: str | None
    siddet: int | None
    alternatif: str | None
    yansitma: str
    alinti: str | None
    adim: str | None
    quote_was_stripped: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GroundedSynthesisResult:
    """Validated structured output for multi-source research synthesis."""

    summary: str
    claims: list[dict[str, Any]]
    total_claims: int
    grounded_claims: int
    dropped_claims: int
    grounding_rate: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_json_object(raw_text: str | None) -> dict[str, Any] | None:
    """Extract a single top-level JSON object from model output without fabrication.

    Strips reasoning blocks (``<think>...</think>``) emitted by open-weight
    thinking models (DeepSeek-R1, Qwen3, Mistral) before parsing.
    """
    if not raw_text:
        return None

    without_think = _THINK_BLOCK_RE.sub("", raw_text).strip()
    cleaned = _FENCE_END_RE.sub("", _FENCE_START_RE.sub("", without_think)).strip()
    candidates: list[str] = [cleaned]

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        sliced = cleaned[start : end + 1]
        if sliced != cleaned:
            candidates.append(sliced)

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            continue

    # Scan backwards from the last '{' using raw_decode when prose trails/precedes JSON.
    decoder = json.JSONDecoder()
    for pos in reversed([i for i, ch in enumerate(cleaned) if ch == "{"]):
        try:
            obj, _ = decoder.raw_decode(cleaned[pos:])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue

    return None


def validate_reflection(payload: dict[str, Any] | None, source_text: str) -> ReflectionResult | None:
    """Validate reflection schema and enforce verbatim quote-grounding.

    Returns ``None`` on malformed schema (never emits synthetic fallback text).
    If ``alinti`` is present in ``payload`` but does not appear verbatim in
    ``source_text``, ``alinti`` is stripped to ``None`` and
    ``quote_was_stripped`` is set to ``True``.
    """
    if not isinstance(payload, dict):
        return None

    yansitma_raw = payload.get("yansitma")
    yansitma = yansitma_raw.strip() if isinstance(yansitma_raw, str) else ""
    if len(yansitma) < 12 or len(yansitma) > 900:
        return None

    adim_raw = payload.get("adim")
    if adim_raw is None:
        adim_raw = payload.get("adım")
    adim = adim_raw.strip()[:220] if isinstance(adim_raw, str) and adim_raw.strip() else None

    alinti_raw = payload.get("alinti")
    if alinti_raw is None:
        alinti_raw = payload.get("alıntı")
    had_candidate_quote = isinstance(alinti_raw, str) and bool(alinti_raw.strip())
    verified_quote = (
        verify_quote_grounding(source_text, alinti_raw, max_chars=240)
        if had_candidate_quote
        else None
    )
    quote_was_stripped = had_candidate_quote and (verified_quote is None)

    siddet_val = payload.get("siddet")
    siddet: int | None = None
    if isinstance(siddet_val, (int, float)) and not isinstance(siddet_val, bool):
        siddet = min(5, max(1, round(float(siddet_val))))

    duygu_raw = payload.get("duygu")
    duygu = (
        duygu_raw.strip()
        if isinstance(duygu_raw, str) and 0 < len(duygu_raw.strip()) <= 40
        else None
    )

    alt_raw = payload.get("alternatif")
    alternatif = (
        alt_raw.strip()
        if isinstance(alt_raw, str) and 0 < len(alt_raw.strip()) <= 40
        else None
    )

    return ReflectionResult(
        duygu=duygu,
        siddet=siddet,
        alternatif=alternatif,
        yansitma=yansitma[:600],
        alinti=verified_quote,
        adim=adim,
        quote_was_stripped=quote_was_stripped,
    )


def validate_grounded_synthesis(
    payload: dict[str, Any] | None,
    sources: dict[str, str],
    require_all_grounded: bool = False,
) -> GroundedSynthesisResult | None:
    """Validate multi-source research synthesis output against ``sources``."""
    if not isinstance(payload, dict):
        return None

    summary_raw = payload.get("summary")
    summary = summary_raw.strip() if isinstance(summary_raw, str) else ""
    if len(summary) < 8:
        return None

    raw_claims = payload.get("claims")
    if not isinstance(raw_claims, list):
        return None

    report: CitationReport = verify_cited_claims(sources, raw_claims)
    if require_all_grounded and report.dropped_claims > 0:
        return None

    verified_dicts = [
        {
            "claim": c.claim,
            "source_id": c.source_id,
            "quote": c.exact_quote,
            "start": c.start,
            "end": c.end,
        }
        for c in report.verified
    ]

    return GroundedSynthesisResult(
        summary=summary[:2000],
        claims=verified_dicts,
        total_claims=report.total_claims,
        grounded_claims=report.grounded_claims,
        dropped_claims=report.dropped_claims,
        grounding_rate=report.grounding_rate,
    )
