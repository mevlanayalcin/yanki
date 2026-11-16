"""Deterministic verbatim quote-grounding and multi-source citation verifier."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .normalize import build_normalized_view, normalize_tr

_WORD_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class SpanMatch:
    """Result of verifying a candidate quote against a source passage."""

    grounded: bool
    start: int | None
    end: int | None
    exact_quote: str | None
    lexical_overlap: float
    reason: str


@dataclass(frozen=True)
class VerifiedClaim:
    """A structured claim verified (or rejected) against primary source text."""

    claim: str
    source_id: str
    grounded: bool
    exact_quote: str | None
    start: int | None
    end: int | None
    lexical_overlap: float
    reason: str


@dataclass(frozen=True)
class CitationReport:
    """Aggregate verification outcome over a list of cited claims."""

    total_claims: int
    grounded_claims: int
    dropped_claims: int
    grounding_rate: float
    verified: tuple[VerifiedClaim, ...]
    rejected: tuple[VerifiedClaim, ...]


def _token_overlap(source_norm: str, quote_norm: str) -> float:
    q_tokens = _WORD_RE.findall(quote_norm)
    if not q_tokens:
        return 0.0
    s_set = set(_WORD_RE.findall(source_norm))
    if not s_set:
        return 0.0
    hits = sum(1 for tok in q_tokens if tok in s_set)
    return round(hits / len(q_tokens), 4)


def find_verbatim_span(source_text: str, candidate_quote: str | None) -> SpanMatch:
    """Verify that ``candidate_quote`` occurs as a contiguous substring of ``source_text``."""
    if candidate_quote is None or not candidate_quote.strip():
        return SpanMatch(
            grounded=False,
            start=None,
            end=None,
            exact_quote=None,
            lexical_overlap=0.0,
            reason="empty_quote",
        )

    src_view = build_normalized_view(source_text)
    q_norm = normalize_tr(candidate_quote)
    if not src_view.text or not q_norm:
        return SpanMatch(
            grounded=False,
            start=None,
            end=None,
            exact_quote=None,
            lexical_overlap=0.0,
            reason="empty_normalized_text",
        )

    pos = src_view.text.find(q_norm)
    if pos >= 0:
        raw_start, raw_end = src_view.source_span(pos, pos + len(q_norm))
        return SpanMatch(
            grounded=True,
            start=raw_start,
            end=raw_end,
            exact_quote=source_text[raw_start:raw_end],
            lexical_overlap=1.0,
            reason="exact_span_match",
        )

    trimmed = candidate_quote.strip().strip("\"'“”‘’«»").rstrip(".").strip()
    q_trimmed = normalize_tr(trimmed)
    if q_trimmed and len(q_trimmed) >= 4:
        pos2 = src_view.text.find(q_trimmed)
        if pos2 >= 0:
            raw_start, raw_end = src_view.source_span(pos2, pos2 + len(q_trimmed))
            return SpanMatch(
                grounded=True,
                start=raw_start,
                end=raw_end,
                exact_quote=source_text[raw_start:raw_end],
                lexical_overlap=1.0,
                reason="trimmed_punctuation_match",
            )

    overlap = _token_overlap(src_view.text, q_norm)
    reason = "paraphrased_not_verbatim" if overlap >= 0.6 else "ungrounded_fabrication"
    return SpanMatch(
        grounded=False,
        start=None,
        end=None,
        exact_quote=None,
        lexical_overlap=overlap,
        reason=reason,
    )


def verify_quote_grounding(
    source_text: str,
    candidate_quote: str | None,
    max_chars: int = 240,
) -> str | None:
    """Return the verified source slice if grounded, else ``None``."""
    match = find_verbatim_span(source_text, candidate_quote)
    if not match.grounded or not match.exact_quote:
        return None
    return match.exact_quote[:max_chars]


def verify_cited_claims(
    sources: dict[str, str],
    claims: list[dict[str, str | None]],
) -> CitationReport:
    """Verify multi-source research synthesis claims against ``sources``."""
    verified: list[VerifiedClaim] = []
    rejected: list[VerifiedClaim] = []

    for item in claims:
        claim_text = str(item.get("claim") or "").strip()
        source_id = str(item.get("source_id") or "").strip()
        quote_text = item.get("quote")

        if not claim_text:
            continue

        if source_id not in sources:
            rejected.append(
                VerifiedClaim(
                    claim=claim_text,
                    source_id=source_id,
                    grounded=False,
                    exact_quote=None,
                    start=None,
                    end=None,
                    lexical_overlap=0.0,
                    reason="unknown_source_id",
                )
            )
            continue

        span = find_verbatim_span(sources[source_id], quote_text)
        record = VerifiedClaim(
            claim=claim_text,
            source_id=source_id,
            grounded=span.grounded,
            exact_quote=span.exact_quote,
            start=span.start,
            end=span.end,
            lexical_overlap=span.lexical_overlap,
            reason=span.reason,
        )
        if span.grounded:
            verified.append(record)
        else:
            rejected.append(record)

    total = len(verified) + len(rejected)
    rate = round(len(verified) / total, 4) if total > 0 else 1.0
    return CitationReport(
        total_claims=total,
        grounded_claims=len(verified),
        dropped_claims=len(rejected),
        grounding_rate=rate,
        verified=tuple(verified),
        rejected=tuple(rejected),
    )
