"""Yankı: deterministic quote-grounding, safety gating, and LLM schema verification."""

from .grounding import (
    CitationReport,
    SpanMatch,
    VerifiedClaim,
    find_verbatim_span,
    verify_cited_claims,
    verify_quote_grounding,
)
from .guardrails import GateDecision, check_crisis_gate
from .normalize import NormalizedView, build_normalized_view, normalize_tr
from .providers import GroundedPipeline, HTTPInferenceBackend, ProviderConfig, ProviderResponse
from .schema import (
    GroundedSynthesisResult,
    ReflectionResult,
    extract_json_object,
    validate_grounded_synthesis,
    validate_reflection,
)

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "CitationReport",
    "GateDecision",
    "GroundedPipeline",
    "GroundedSynthesisResult",
    "HTTPInferenceBackend",
    "NormalizedView",
    "ProviderConfig",
    "ProviderResponse",
    "ReflectionResult",
    "SpanMatch",
    "VerifiedClaim",
    "build_normalized_view",
    "check_crisis_gate",
    "extract_json_object",
    "find_verbatim_span",
    "normalize_tr",
    "validate_grounded_synthesis",
    "validate_reflection",
    "verify_cited_claims",
    "verify_quote_grounding",
]
