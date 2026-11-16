"""Deterministic pre-inference safety and crisis lexical gate.

Mirrors ``krizMi()`` in ``cloudflare/worker.mjs`` so edge requests and offline
GPU evaluation runs share identical pre-inference short-circuit semantics.
When a pattern triggers, no LLM call is issued.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .normalize import normalize_tr

CRISIS_PATTERNS: tuple[str, ...] = (
    "intihar",
    "kendimi oldur",
    "oldurmek istiyorum",
    "yasamak istemiyorum",
    "yashamak istemiyorum",
    "hayati birak",
    "kendime zarar",
    "kendime ziyan",
    "kendimi parcala",
    "kill myself",
    "suicide",
    "end my life",
    "want to die",
    "harm myself",
    "not worth living",
)

CRISIS_RESPONSES: dict[str, str] = {
    "tr": (
        "Yazdıkların günlük bir yansıtmanın dışında duruyor. Şu anda güvende değilsen "
        "ya da kendini yaralamayı düşünüyorsan Türkiye'de 112'yi ara. Bir uzmana ya da "
        "güvendiğin birine ulaşmak için yazman yeterli — bu kutu sana cevap vermesin, sen bir insana ulaş."
    ),
    "en": (
        "What you wrote sits outside a daily reflection. If you are not safe right now, "
        "or you are thinking of harming yourself, call 112 in Türkiye or your local "
        "emergency number. Reach a person — this box is not the one that should answer."
    ),
}

CRISIS_DISCLAIMERS: dict[str, str] = {
    "tr": "Yankı terapi değildir. Kriz sözcükleri kural listesiyle yakalanır; bu yanıtta model çağrılmadı.",
    "en": "Yankı is not therapy. Crisis wording is caught by a rule list; no model was called for this answer.",
}

_PUNCT_CLEAN_RE = re.compile(r"[^\w\s]+", flags=re.UNICODE)


@dataclass(frozen=True)
class GateDecision:
    """Outcome of the pre-inference safety gate."""

    triggered: bool
    matched_pattern: str | None
    response_text: str | None
    disclaimer: str | None


def check_crisis_gate(text: str, lang: str = "en") -> GateDecision:
    """Check ``text`` against deterministic pre-inference crisis patterns.

    Uses Turkish-normalized prefix/word-boundary matching consistent with
    ``cloudflare/worker.mjs`` while stripping punctuation so forms like
    ``"İntihar,"`` or ``"yaşamak istemiyorum."`` match reliably.
    """
    resolved_lang = "tr" if lang == "tr" else "en"
    cleaned = _PUNCT_CLEAN_RE.sub(" ", text or "")
    padded = " " + normalize_tr(cleaned) + " "

    for pat in CRISIS_PATTERNS:
        norm_pat = normalize_tr(pat)
        if (" " + norm_pat + " ") in padded or (" " + norm_pat) in padded:
            return GateDecision(
                triggered=True,
                matched_pattern=norm_pat,
                response_text=CRISIS_RESPONSES[resolved_lang],
                disclaimer=CRISIS_DISCLAIMERS[resolved_lang],
            )

    return GateDecision(
        triggered=False,
        matched_pattern=None,
        response_text=None,
        disclaimer=None,
    )
