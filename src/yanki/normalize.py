"""Turkish-aware Unicode normalization with exact character-offset provenance.

Standard Python ``str.lower()`` turns ``'İ'`` (U+0130) into the two-codepoint
sequence ``'i\\u0307'``, which shifts string indices and breaks slice recovery
on original UTF-8 documents. ``build_normalized_view`` folds Turkish and Latin
diacritics into a canonical single-space ASCII/base representation while
recording the exact start and end character offsets in the raw source text.
"""

from __future__ import annotations

from dataclasses import dataclass
import unicodedata

_TR_CHAR_MAP: dict[str, str] = {
    "ğ": "g",
    "Ğ": "g",
    "ü": "u",
    "Ü": "u",
    "ş": "s",
    "Ş": "s",
    "ı": "i",
    "I": "i",
    "İ": "i",
    "ö": "o",
    "Ö": "o",
    "ç": "c",
    "Ç": "c",
    "â": "a",
    "Â": "a",
    "î": "i",
    "Î": "i",
    "û": "u",
    "Û": "u",
}


@dataclass(frozen=True)
class NormalizedView:
    """Normalized string paired with per-character source index bounds."""

    text: str
    starts: tuple[int, ...]
    ends: tuple[int, ...]

    def source_span(self, norm_start: int, norm_end: int) -> tuple[int, int]:
        """Map ``[norm_start, norm_end)`` back to raw source ``[start, end)``."""
        if norm_start < 0 or norm_end > len(self.text) or norm_start >= norm_end:
            raise ValueError(f"Invalid normalized span [{norm_start}, {norm_end}) for length {len(self.text)}")
        return self.starts[norm_start], self.ends[norm_end - 1]


def _fold_char(ch: str) -> str:
    if ch in _TR_CHAR_MAP:
        return _TR_CHAR_MAP[ch]
    decomposed = unicodedata.normalize("NFKD", ch)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    out: list[str] = []
    for c in stripped:
        if c in _TR_CHAR_MAP:
            out.append(_TR_CHAR_MAP[c])
        else:
            low = c.lower()
            out.append("".join(x for x in low if not unicodedata.combining(x)))
    return "".join(out)


def build_normalized_view(raw: str | None) -> NormalizedView:
    """Fold ``raw`` into normalized lowercase text while preserving offsets.

    Whitespace runs collapse to a single ASCII space and leading/trailing
    whitespace is stripped, matching ``normalizle()`` in ``cloudflare/worker.mjs``
    while keeping exact raw-string character provenance.
    """
    if not raw:
        return NormalizedView(text="", starts=(), ends=())

    chars: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    pending_space_start: int | None = None
    pending_space_end: int = 0

    for idx, ch in enumerate(raw):
        if ch.isspace():
            if chars and pending_space_start is None:
                pending_space_start = idx
            if chars:
                pending_space_end = idx + 1
            continue

        folded = _fold_char(ch)
        if not folded:
            continue

        if pending_space_start is not None:
            chars.append(" ")
            starts.append(pending_space_start)
            ends.append(pending_space_end)
            pending_space_start = None

        for fc in folded:
            chars.append(fc)
            starts.append(idx)
            ends.append(idx + 1)

    return NormalizedView(
        text="".join(chars),
        starts=tuple(starts),
        ends=tuple(ends),
    )


def normalize_tr(text: str | None) -> str:
    """Return the normalized Turkish/English string without offset tables."""
    return build_normalized_view(text).text
