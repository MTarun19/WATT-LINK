
from __future__ import annotations

import os
from typing import Optional

from .llm_client import LLMClient, LLMProvider
from .parser import DecisionParser, AgentDecision, DecisionParseError
from .memory import MemoryStore, MemoryRecord
from .prompts import (
    SYSTEM_PROMPT_AGENT,
    SYSTEM_PROMPT_MANAGER,
    build_agent_user_prompt,
    build_manager_user_prompt,
)

__all__ = [
    "LLMClient",
    "LLMProvider",
    "DecisionParser",
    "AgentDecision",
    "DecisionParseError",
    "MemoryStore",
    "MemoryRecord",
    "SYSTEM_PROMPT_AGENT",
    "SYSTEM_PROMPT_MANAGER",
    "build_agent_user_prompt",
    "build_manager_user_prompt",
    "get_llm_client",
]


def get_llm_client() -> LLMClient:
    """Build a configured ``LLMClient`` from environment variables.

    Resolved variables
    ------------------
    LLM_PROVIDER        "openai" (default) or "ollama"
    OPENAI_API_KEY       Required when provider is openai
    OPENAI_MODEL         OpenAI model name (default: gpt-4o-mini)
    OPENAI_BASE_URL      Optional OpenAI-compatible base URL override
    OLLAMA_HOST          Ollama server URL (default: http://localhost:11434)
    OLLAMA_MODEL         Ollama model name (default: llama3)

    Returns
    -------
    LLMClient
        Ready-to-use client instance.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower().strip()
    if provider == "ollama":
        return LLMClient(
            provider=LLMProvider.OLLAMA,
            model=os.getenv("OLLAMA_MODEL", "llama3"),
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        )
    # Default: OpenAI (or any OpenAI-compatible endpoint)
    return LLMClient(
        provider=LLMProvider.OPENAI,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
    )


__version__ = "1.0.0"
