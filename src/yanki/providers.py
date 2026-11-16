"""Multi-provider inference client and grounded router.

Supports both OpenAI-compatible inference servers (local/cluster ``vLLM``,
``SGLang``, ``NVIDIA NIM``, ``Fireworks``) and the Anthropic Messages API using
Python's standard library HTTP stack so evaluation jobs run in air-gapped HPC
containers without proprietary SDK dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import time
from typing import Any, Protocol
import urllib.error
import urllib.request

from .guardrails import check_crisis_gate
from .schema import extract_json_object, validate_grounded_synthesis, validate_reflection

REFLECTION_SYSTEM_PROMPT = (
    "You are Yankı, an emotional check-in companion. You are not a therapist, "
    "you do not diagnose, and you never advise on medication.\n\n"
    "Read the user's passage and answer with ONE JSON object and nothing else:\n"
    '{"duygu": "one feeling word in the user\'s language", '
    '"siddet": 1, '
    '"alternatif": "the feeling you considered and rejected, or null", '
    '"yansitma": "one or two sentences in the user\'s language reflecting what you hear, addressed to \'you\'", '
    '"alinti": "an exact contiguous substring copied from the user\'s passage that carries the feeling, or null", '
    '"adim": "one concrete action doable within the next hour, in the user\'s language"}\n\n'
    "Rules:\n"
    '- "alinti" must be copied character-for-character from the user\'s passage. '
    "If you cannot find such a sentence, use null. Never paraphrase inside \"alinti\".\n"
    "- Name at most one feeling. Do not add advice about diagnosis, medication or therapy.\n"
    "- Keep \"yansitma\" under 45 words and \"adim\" under 22 words."
)

SYNTHESIS_SYSTEM_PROMPT = (
    "You are a primary-source synthesis engine. Answer ONLY from the provided sources "
    "and emit ONE JSON object with keys:\n"
    '{"summary": "concise synthesis", "claims": [{"claim": "...", "source_id": "...", '
    '"quote": "exact contiguous substring copied verbatim from that source"}]}\n'
    "Never paraphrase inside \"quote\". Omit any claim you cannot back with an exact quote."
)


@dataclass(frozen=True)
class ProviderResponse:
    """Raw completion text and telemetry returned by an inference backend."""

    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float


class InferenceBackend(Protocol):
    def complete(self, system: str, user_message: str, max_tokens: int = 640, temperature: float = 0.2) -> ProviderResponse:
        ...


@dataclass(frozen=True)
class ProviderConfig:
    """Configuration for an OpenAI-compatible (vLLM/SGLang/NIM) or Anthropic endpoint."""

    kind: str  # "openai-compat" | "anthropic"
    model: str
    base_url: str
    api_key: str = ""
    timeout_sec: float = 60.0

    @classmethod
    def from_env(cls, kind: str = "openai-compat") -> "ProviderConfig":
        if kind == "anthropic":
            return cls(
                kind="anthropic",
                model=os.environ.get("YANKI_MODEL", "claude-haiku-4-5-20251001"),
                base_url=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1/messages"),
                api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            )
        return cls(
            kind="openai-compat",
            model=os.environ.get("YANKI_MODEL", "Qwen/Qwen2.5-32B-Instruct"),
            base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1"),
            api_key=os.environ.get("OPENAI_API_KEY", "EMPTY"),
        )


class HTTPInferenceBackend:
    """Standard-library HTTP adapter for OpenAI-compatible and Anthropic APIs."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def complete(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 1536,
        temperature: float = 0.2,
    ) -> ProviderResponse:
        t0 = time.perf_counter()
        if self.config.kind == "anthropic":
            url = self.config.base_url
            headers = {
                "content-type": "application/json",
                "user-agent": "yanki/0.2.0",
                "anthropic-version": "2023-06-01",
                "x-api-key": self.config.api_key,
            }
            payload: dict[str, Any] = {
                "model": self.config.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "system": system,
                "messages": [{"role": "user", "content": user_message}],
            }
        else:
            base = self.config.base_url.rstrip("/")
            url = base if base.endswith("/chat/completions") else f"{base}/chat/completions"
            headers = {
                "content-type": "application/json",
                "user-agent": "yanki/0.2.0",
            }
            if self.config.api_key:
                headers["authorization"] = f"Bearer {self.config.api_key}"
            payload = {
                "model": self.config.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
            }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout_sec) as resp:
                raw_body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise RuntimeError(f"Upstream HTTP {exc.code}: {detail}") from exc

        latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        data = json.loads(raw_body)

        if self.config.kind == "anthropic":
            blocks = data.get("content") or []
            text = " ".join(b.get("text", "") for b in blocks if b.get("type") == "text")
            usage = data.get("usage") or {}
            in_tok = int(usage.get("input_tokens") or 0)
            out_tok = int(usage.get("output_tokens") or 0)
        else:
            choices = data.get("choices") or [{}]
            msg = choices[0].get("message") or {}
            text = str(msg.get("content") or "")
            usage = data.get("usage") or {}
            in_tok = int(usage.get("prompt_tokens") or 0)
            out_tok = int(usage.get("completion_tokens") or 0)

        return ProviderResponse(
            text=text,
            provider=self.config.kind,
            model=self.config.model,
            input_tokens=in_tok,
            output_tokens=out_tok,
            latency_ms=latency_ms,
        )


class GroundedPipeline:
    """End-to-end safety-gated, schema-validated, quote-grounded pipeline."""

    def __init__(self, backend: InferenceBackend) -> None:
        self.backend = backend

    def reflect(self, passage: str, lang: str = "en") -> dict[str, Any]:
        clean = " ".join((passage or "").split())
        if len(clean) < 8:
            raise ValueError("Input passage must be at least 8 characters.")
        if len(clean) > 600:
            raise ValueError("Input passage exceeds 600 characters.")

        resolved_lang = "tr" if lang == "tr" else "en"
        gate = check_crisis_gate(clean, lang=resolved_lang)
        if gate.triggered:
            return {
                "kriz": True,
                "matched_pattern": gate.matched_pattern,
                "yansitma": gate.response_text,
                "duygu": None,
                "siddet": None,
                "alinti": None,
                "adim": None,
                "disclaimer": gate.disclaimer,
                "provider": "rule",
                "model": "crisis-list-v1",
            }

        prefix = "Kullanıcının günlüğü (Türkçe):" if resolved_lang == "tr" else "The user's journal entry (English):"
        prompt = f'{prefix}\n"""{clean}"""\nAnswer with the JSON object only.'
        resp = self.backend.complete(REFLECTION_SYSTEM_PROMPT, prompt)
        validated = validate_reflection(extract_json_object(resp.text), clean)
        if validated is None:
            raise RuntimeError("Model output failed strict JSON reflection schema validation.")

        out = validated.to_dict()
        out.update(
            {
                "kriz": False,
                "provider": resp.provider,
                "model": resp.model,
                "latency_ms": resp.latency_ms,
                "usage": {
                    "input_tokens": resp.input_tokens,
                    "output_tokens": resp.output_tokens,
                },
            }
        )
        return out

    def synthesize_sources(
        self,
        question: str,
        sources: dict[str, str],
        require_all_grounded: bool = False,
    ) -> dict[str, Any]:
        rendered_sources = "\n\n".join(
            f"[SOURCE {sid}]\n{body}" for sid, body in sources.items()
        )
        prompt = f"Question: {question}\n\nSources:\n{rendered_sources}\n\nReturn JSON only."
        resp = self.backend.complete(SYNTHESIS_SYSTEM_PROMPT, prompt, max_tokens=1024)
        validated = validate_grounded_synthesis(
            extract_json_object(resp.text),
            sources,
            require_all_grounded=require_all_grounded,
        )
        if validated is None:
            raise RuntimeError("Model output failed grounded synthesis schema validation.")

        out = validated.to_dict()
        out.update(
            {
                "provider": resp.provider,
                "model": resp.model,
                "latency_ms": resp.latency_ms,
                "usage": {
                    "input_tokens": resp.input_tokens,
                    "output_tokens": resp.output_tokens,
                },
            }
        )
        return out
