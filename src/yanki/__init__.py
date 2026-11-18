"""Yankı: deterministic quote-grounding, safety gating, and LLM schema verification."""

from .finetune import (
    PreferenceExample,
    SFTExample,
    build_alignment_examples,
    corrupt_verbatim_quote,
    export_alignment_jsonl,
    verify_preference_pair,
)
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
from .train import TrainingConfig, compute_reference_free_dpo_loss_scalar, load_jsonl_records

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "CitationReport",
    "GateDecision",
    "GroundedPipeline",
    "GroundedSynthesisResult",
    "HTTPInferenceBackend",
    "NormalizedView",
    "PreferenceExample",
    "ProviderConfig",
    "ProviderResponse",
    "ReflectionResult",
    "SFTExample",
    "SpanMatch",
    "TrainingConfig",
    "VerifiedClaim",
    "build_alignment_examples",
    "build_normalized_view",
    "check_crisis_gate",
    "compute_reference_free_dpo_loss_scalar",
    "corrupt_verbatim_quote",
    "export_alignment_jsonl",
    "extract_json_object",
    "find_verbatim_span",
    "load_jsonl_records",
    "normalize_tr",
    "validate_grounded_synthesis",
    "validate_reflection",
    "verify_cited_claims",
    "verify_preference_pair",
    "verify_quote_grounding",
]
