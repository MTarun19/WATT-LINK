"""Provider-agnostic LLM client for WATT LINK.

Supports two backends, selected at construction time:

* ``LLMProvider.OPENAI``  -> OpenAI Chat Completions API (or any OpenAI-compatible
  endpoint such as Azure OpenAI, LM Studio, vLLM, ...).
* ``LLMProvider.OLLAMA``  -> Ollama ``/api/chat`` endpoint (default model: llama3).

The client only depends on the Python standard library (``urllib``, ``json``)
so it can be dropped into an existing backend without adding a single pip
dependency.  If the ``openai`` package is already installed in the project it is
preferred for OpenAI calls (slightly better retry/timeout handling), but it is
strictly optional.

Usage
-----
>>> from backend.llm import LLMClient, LLMProvider
>>> client = LLMClient(LLMProvider.OLLAMA, model="llama3", host="http://localhost:11434")
>>> text = client.complete("You are a helpful assistant.", "Summarise this sensor row.")
"""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Supported LLM backends."""

    OPENAI = "openai"
    OLLAMA = "ollama"


class LLMError(RuntimeError):
    """Raised when the LLM backend returns an error or is unreachable."""


@dataclass
class LLMConfig:
    """Runtime configuration for an ``LLMClient``."""

    provider: LLMProvider = LLMProvider.OPENAI
    model: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: Optional[str] = None
    host: str = "http://localhost:11434"
    temperature: float = 0.2
    max_tokens: int = 1024
    request_timeout: float = 60.0
    max_retries: int = 3
    backoff_base: float = 1.5


@dataclass
class LLMResponse:
    """Normalised completion result."""

    text: str
    raw: Dict[str, Any] = field(default_factory=dict)
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = ""

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.text


class LLMClient:
    """Minimal, dependency-free client for OpenAI and Ollama chat models.

    Parameters
    ----------
    provider
        Which backend to talk to.
    model
        Model identifier (e.g. ``"gpt-4o-mini"`` or ``"llama3"``).
    api_key
        Required for the OpenAI provider; ignored by Ollama.
    base_url
        Optional override for the OpenAI endpoint (e.g. an OpenAI-compatible
        proxy).  Defaults to the public OpenAI API.
    host
        Base URL of the Ollama server (ignored by the OpenAI provider).
    **kwargs
        Any other ``LLMConfig`` fields (``temperature``, ``max_tokens`` ...).
    """

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        model: str = "gpt-4o-mini",
        api_key: str = "",
        base_url: Optional[str] = None,
        host: str = "http://localhost:11434",
        **kwargs: Any,
    ) -> None:
        self.config = LLMConfig(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            host=host,
            **{k: v for k, v in kwargs.items() if hasattr(LLMConfig, k)},  # type: ignore[arg-type]
        )
        # Lazy: only imported when an OpenAI call is actually made.
        self._openai_module: Any = None

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def complete(
        self,
        system: str,
        user: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Return the assistant's text completion for ``system`` + ``user``.

        Raises
        ------
        LLMError
            If the backend is unreachable or returns an error after all
            retries are exhausted.
        """
        response = self._complete_raw(system, user, temperature, max_tokens)
        return response.text

    def complete_json(
        self,
        system: str,
        user: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Return the completion parsed as a JSON object.

        Falls back to ``{}`` if the model output is not valid JSON; callers that
        need strict parsing should use ``backend.llm.parser.DecisionParser``.
        """
        text = self.complete(system, user, temperature=temperature, max_tokens=max_tokens)
        return _safe_json_loads(text)

    # ------------------------------------------------------------------ #
    # Internal dispatch
    # ------------------------------------------------------------------ #
    def _complete_raw(
        self,
        system: str,
        user: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> LLMResponse:
        cfg = self.config
        temp = cfg.temperature if temperature is None else temperature
        tokens = cfg.max_tokens if max_tokens is None else max_tokens

        if cfg.provider is LLMProvider.OLLAMA:
            return self._call_ollama(system, user, temp, tokens)
        return self._call_openai(system, user, temp, tokens)

    # ------------------------------------------------------------------ #
    # OpenAI
    # ------------------------------------------------------------------ #
    def _call_openai(
        self,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        # Prefer the official SDK if it's available.
        if self._openai_module is None:
            try:
                import openai  # type: ignore

                self._openai_module = openai
            except ImportError:
                self._openai_module = False

        if self._openai_module:
            return self._call_openai_sdk(system, user, temperature, max_tokens)
        return self._call_openai_http(system, user, temperature, max_tokens)

    def _call_openai_sdk(
        self,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        openai = self._openai_module
        cfg = self.config
        base_url = cfg.base_url
        api_key = cfg.api_key or "missing-key"
        try:
            client_kwargs: Dict[str, Any] = {"api_key": api_key}
            if base_url:
                client_kwargs["base_url"] = base_url
            client = openai.OpenAI(**client_kwargs)  # type: ignore[attr-defined]
        except AttributeError:  # older openai<1.0 layout
            return self._call_openai_http(system, user, temperature, max_tokens)

        last_err: Optional[Exception] = None
        for attempt in range(cfg.max_retries):
            try:
                resp = client.chat.completions.create(  # type: ignore[union-attr]
                    model=cfg.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                text = resp.choices[0].message.content or ""
                return LLMResponse(
                    text=text,
                    raw=resp.model_dump() if hasattr(resp, "model_dump") else {},
                    provider=LLMProvider.OPENAI,
                    model=cfg.model,
                )
            except Exception as exc:  # noqa: BLE001 - SDK raises varied types
                last_err = exc
                _backoff(attempt, cfg.backoff_base)
        raise LLMError(f"OpenAI request failed after {cfg.max_retries} retries: {last_err}")

    def _call_openai_http(
        self,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        cfg = self.config
        url = cfg.base_url or "https://api.openai.com/v1/chat/completions"
        payload: Dict[str, Any] = {
            "model": cfg.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg.api_key}",
        }
        raw = self._http_post(url, payload, headers, cfg)
        try:
            text = raw["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected OpenAI response shape: {exc}") from exc
        return LLMResponse(
            text=text,
            raw=raw,
            provider=LLMProvider.OPENAI,
            model=cfg.model,
        )

    # ------------------------------------------------------------------ #
    # Ollama
    # ------------------------------------------------------------------ #
    def _call_ollama(
        self,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        cfg = self.config
        url = f"{cfg.host.rstrip('/')}/api/chat"
        payload: Dict[str, Any] = {
            "model": cfg.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        headers = {"Content-Type": "application/json"}
        raw = self._http_post(url, payload, headers, cfg)
        try:
            text = raw.get("message", {}).get("content", "") or raw.get("response", "")
        except (AttributeError, TypeError) as exc:
            raise LLMError(f"Unexpected Ollama response shape: {exc}") from exc
        return LLMResponse(
            text=text,
            raw=raw,
            provider=LLMProvider.OLLAMA,
            model=cfg.model,
        )

    # ------------------------------------------------------------------ #
    # Shared HTTP helper (stdlib only)
    # ------------------------------------------------------------------ #
    def _http_post(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        cfg: LLMConfig,
    ) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        last_err: Optional[Exception] = None
        for attempt in range(cfg.max_retries):
            try:
                req = urllib.request.Request(  # noqa: S310 - trusted internal endpoint
                    url,
                    data=data,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=cfg.request_timeout) as resp:  # noqa: S310
                    body = resp.read().decode("utf-8")
                    return json.loads(body)
            except urllib.error.HTTPError as exc:
                body = ""
                try:
                    body = exc.read().decode("utf-8", errors="replace")
                except Exception:  # noqa: BLE001
                    pass
                # 4xx (except 429) are not retryable.
                if exc.code != 429 and 400 <= exc.code < 500:
                    raise LLMError(f"LLM HTTP {exc.code}: {body}") from exc
                last_err = exc
                _backoff(attempt, cfg.backoff_base)
            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
                last_err = exc
                _backoff(attempt, cfg.backoff_base)
            except Exception as exc:  # noqa: BLE001 - last-resort guard
                last_err = exc
                _backoff(attempt, cfg.backoff_base)
        raise LLMError(
            f"LLM request to {url} failed after {cfg.max_retries} retries: {last_err}"
        )


# ---------------------------------------------------------------------- #
# Module-level helpers
# ---------------------------------------------------------------------- #
def _backoff(attempt: int, base: float) -> None:
    """Sleep for ``base ** attempt`` seconds (capped at ~20s)."""
    delay = min(base ** attempt, 20.0)
    if delay > 0:
        time.sleep(delay)


def _safe_json_loads(text: str) -> Dict[str, Any]:
    """Best-effort JSON parse; returns ``{}`` on failure."""
    try:
        loaded = json.loads(text)
        if isinstance(loaded, dict):
            return loaded
    except (json.JSONDecodeError, TypeError):
        pass
    return {}
