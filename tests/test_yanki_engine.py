"""Unit and integration tests for the Yankı verification and routing engine."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from yanki import (
    GroundedPipeline,
    ProviderConfig,
    ProviderResponse,
    build_normalized_view,
    check_crisis_gate,
    extract_json_object,
    find_verbatim_span,
    normalize_tr,
    validate_grounded_synthesis,
    validate_reflection,
    verify_cited_claims,
    verify_quote_grounding,
)
from yanki.cli import main as cli_main
from yanki.eval import DEFAULT_SUITE, load_suite, run_offline_suite

REPO_ROOT = Path(__file__).resolve().parent.parent


class DummyBackend:
    """Deterministic in-memory backend for testing GroundedPipeline."""

    def __init__(self, canned_text: str, provider: str = "openai-compat", model: str = "Qwen/Qwen2.5-32B-Instruct") -> None:
        self.canned_text = canned_text
        self.provider = provider
        self.model = model
        self.calls: int = 0

    def complete(self, system: str, user_message: str, max_tokens: int = 640, temperature: float = 0.2) -> ProviderResponse:
        self.calls += 1
        return ProviderResponse(
            text=self.canned_text,
            provider=self.provider,
            model=self.model,
            input_tokens=84,
            output_tokens=42,
            latency_ms=12.4,
        )


def test_turkish_dotted_i_offset_mapping_preserves_exact_slice() -> None:
    raw = "İSTANBUL ve Iğdır arasında ışıltılı bir gökyüzü vardı."
    view = build_normalized_view(raw)
    assert view.text == "istanbul ve igdir arasinda isiltili bir gokyuzu vardi."

    target = "isiltili bir gokyuzu"
    idx = view.text.index(target)
    s, e = view.source_span(idx, idx + len(target))
    assert raw[s:e] == "ışıltılı bir gökyüzü"


def test_normalize_tr_collapses_whitespace_and_diacritics() -> None:
    assert normalize_tr("  Çığlık   Üstüne\nŞüphe  ") == "ciglik ustune suphe"
    assert normalize_tr("") == ""
    assert normalize_tr(None) == ""


def test_find_verbatim_span_recovers_original_casing() -> None:
    source = "Sunum sırasında göğsüm sıkıştı ama sonuna kadar devam ettim."
    match = find_verbatim_span(source, "GOGSUM SIKISTI AMA SONUNA KADAR")
    assert match.grounded is True
    assert match.exact_quote == "göğsüm sıkıştı ama sonuna kadar"
    assert source[match.start : match.end] == "göğsüm sıkıştı ama sonuna kadar"


def test_find_verbatim_span_rejects_paraphrase_and_scores_overlap() -> None:
    source = "Akşam kimse aramayınca kendimi gereksiz hissettim."
    match = find_verbatim_span(source, "Kimse aramayınca kendimi çok yalnız hissettim")
    assert match.grounded is False
    assert match.exact_quote is None
    assert match.reason in ("paraphrased_not_verbatim", "ungrounded_fabrication")


def test_verify_quote_grounding_strips_fabricated_quotes() -> None:
    source = "I finished the report at midnight and felt completely drained."
    assert verify_quote_grounding(source, "felt completely drained") == "felt completely drained"
    assert verify_quote_grounding(source, "felt super tired at midnight") is None


def test_crisis_gate_catches_turkish_and_english_patterns_without_llm() -> None:
    tr_hit = check_crisis_gate("İntihar düşüncesi var aklımda, kimseye söyleyemiyorum.", lang="tr")
    assert tr_hit.triggered is True
    assert tr_hit.matched_pattern == "intihar"
    assert "112" in (tr_hit.response_text or "")

    en_hit = check_crisis_gate("Nothing makes sense, I want to end my life.", lang="en")
    assert en_hit.triggered is True
    assert en_hit.matched_pattern == "end my life"

    safe = check_crisis_gate("Toplantı uzadığı için çok yorgunum, biraz yürüyüş yapacağım.", lang="tr")
    assert safe.triggered is False
    assert safe.response_text is None


def test_parity_with_committed_ornekler_json() -> None:
    ornekler_path = REPO_ROOT / "data" / "ornekler.json"
    data: dict[str, list[dict[str, Any]]] = json.loads(ornekler_path.read_text(encoding="utf-8"))

    for lang in ("en", "tr"):
        for item in data[lang]:
            passage = item["girdi"]
            if item["kriz"]:
                gate = check_crisis_gate(passage, lang=lang)
                assert gate.triggered is True, f"Expected crisis trigger for: {passage}"
            else:
                quote = item.get("alıntı") or item.get("alinti")
                if quote:
                    verified = verify_quote_grounding(passage, quote)
                    assert verified is not None, f"Sample quote should ground in passage: {quote}"


def test_extract_json_object_handles_markdown_fences_and_prose_wrappers() -> None:
    wrapped = 'Here is the JSON:\n```json\n{"duygu": "calm", "siddet": 2, "yansitma": "You sound settled right now."}\n```'
    parsed = extract_json_object(wrapped)
    assert parsed is not None
    assert parsed["duygu"] == "calm"

    with_think = '<think>\nLet me check {"draft": 1} first.\n</think>\n{"duygu": "huzur", "siddet": 2, "yansitma": "Sakin bir akşam geçirmişsin."}'
    parsed_think = extract_json_object(with_think)
    assert parsed_think is not None
    assert parsed_think["duygu"] == "huzur"
    assert extract_json_object("not json at all") is None


def test_validate_reflection_enforces_bounds_and_strips_bad_quote() -> None:
    source = "Bütün hafta uykusuz kaldım ama projeyi teslim ettim."
    good = validate_reflection(
        {
            "duygu": "yorgunluk",
            "siddet": 9,  # clamped to 5
            "yansitma": "Yoğun uykusuzluğa rağmen teslimi tamamlamış olman büyük bir yükü geride bırakmış.",
            "alinti": "uykusuz kaldim ama projeyi teslim ettim",
            "adim": "Bu akşam ekranları erken kapatıp dinlen.",
        },
        source,
    )
    assert good is not None
    assert good.siddet == 5
    assert good.alinti == "uykusuz kaldım ama projeyi teslim ettim"
    assert good.quote_was_stripped is False

    halluc = validate_reflection(
        {
            "duygu": "yorgunluk",
            "siddet": 4,
            "yansitma": "Yoğun uykusuzluğa rağmen teslimi tamamlamışsın.",
            "alinti": "hiç uyumadan sabahladım",
            "adim": "Dinlen.",
        },
        source,
    )
    assert halluc is not None
    assert halluc.alinti is None
    assert halluc.quote_was_stripped is True


def test_multi_source_citation_verification_and_synthesis_validator() -> None:
    sources = {
        "paper_a": "Tensor parallelism across four H200 GPUs reduced p95 latency from 410 ms to 118 ms.",
        "paper_b": "All unverified quotations are removed deterministically prior to serialization.",
    }
    payload = {
        "summary": "Multi-GPU serving lowers tail latency while deterministic post-checks drop hallucinated quotes.",
        "claims": [
            {
                "claim": "4x H200 tensor parallelism cut p95 latency to 118 ms.",
                "source_id": "paper_a",
                "quote": "reduced p95 latency from 410 ms to 118 ms",
            },
            {
                "claim": "Hallucinated claim with invented quote.",
                "source_id": "paper_b",
                "quote": "models never make citation errors",
            },
        ],
    }
    res = validate_grounded_synthesis(payload, sources, require_all_grounded=False)
    assert res is not None
    assert res.total_claims == 2
    assert res.grounded_claims == 1
    assert res.dropped_claims == 1
    assert res.grounding_rate == 0.5
    assert validate_grounded_synthesis(payload, sources, require_all_grounded=True) is None

    report = verify_cited_claims(sources, payload["claims"])
    assert len(report.verified) == 1
    assert len(report.rejected) == 1


def test_grounded_pipeline_short_circuits_crisis_before_backend() -> None:
    backend = DummyBackend('{"duygu": "sad", "siddet": 4, "yansitma": "Should never be called."}')
    pipeline = GroundedPipeline(backend)
    out = pipeline.reflect("I feel like I want to end my life tonight.", lang="en")
    assert out["kriz"] is True
    assert out["provider"] == "rule"
    assert backend.calls == 0


def test_grounded_pipeline_validates_live_backend_response() -> None:
    backend = DummyBackend(
        json.dumps(
            {
                "duygu": "relief",
                "siddet": 2,
                "alternatif": "fatigue",
                "yansitma": "Finishing that migration lifted a weight off your shoulders even if you are tired.",
                "alinti": "weight off my shoulders",
                "adim": "Step away from the terminal for twenty minutes.",
            }
        )
    )
    pipeline = GroundedPipeline(backend)
    out = pipeline.reflect("Shipping the migration finally took a weight off my shoulders today.", lang="en")
    assert out["kriz"] is False
    assert out["alinti"] == "weight off my shoulders"
    assert backend.calls == 1


def test_offline_benchmark_suite_achieves_100_percent_contract_accuracy() -> None:
    cases = load_suite(DEFAULT_SUITE)
    assert len(cases) >= 24
    report = run_offline_suite(cases)
    assert report["failures"] == []
    assert report["span_accuracy"] == 1.0
    assert report["hallucination_rejection_rate"] == 1.0
    assert report["crisis_recall"] == 1.0
    assert report["crisis_false_positive_rate"] == 0.0
    assert report["schema_contract_accuracy"] == 1.0
    assert report["multi_source_rag_accuracy"] == 1.0


def test_cli_verify_and_eval_commands(capsys: pytest.CaptureFixture[str]) -> None:
    rc_ok = cli_main(["verify", "--source", "İstanbul sabahı çok sessizdi.", "--quote", "istanbul sabahi"])
    assert rc_ok == 0
    captured = json.loads(capsys.readouterr().out)
    assert captured["grounded"] is True
    assert captured["exact_quote"] == "İstanbul sabahı"

    rc_bad = cli_main(["verify", "--source", "İstanbul sabahı çok sessizdi.", "--quote", "ankara aksami"])
    assert rc_bad == 2
    _ = capsys.readouterr()

    rc_eval = cli_main(["eval", "--offline", "--strict-thresholds"])
    assert rc_eval == 0


def test_provider_config_from_env_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("YANKI_MODEL", raising=False)
    cfg_vllm = ProviderConfig.from_env("openai-compat")
    assert cfg_vllm.kind == "openai-compat"
    assert cfg_vllm.base_url.endswith("/v1")

    cfg_anth = ProviderConfig.from_env("anthropic")
    assert cfg_anth.kind == "anthropic"
