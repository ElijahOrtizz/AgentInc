"""
Provider factory.

The rest of the backend calls get_provider() to get the active LLM provider.
Which provider is returned depends entirely on the LLM_PROVIDER env var.

This is the only place that knows about concrete provider classes.
Routes and health checks stay provider-agnostic.
"""

import os
from functools import lru_cache
from backend.services.providers.base import BaseProvider


@lru_cache(maxsize=1)
def get_provider() -> BaseProvider:
    """
    Return the configured provider instance.

    Uses lru_cache so the provider is instantiated once and reused.
    Call get_provider.cache_clear() in tests if you need to reset it.

    Supported values for LLM_PROVIDER:
        ollama     — local Ollama server (default, free)
        anthropic  — Anthropic cloud API (requires ANTHROPIC_API_KEY)
    """
    provider_name = os.getenv("LLM_PROVIDER", "ollama").lower().strip()

    if provider_name == "ollama":
        from backend.services.providers.ollama import OllamaProvider
        return OllamaProvider()

    if provider_name == "anthropic":
        from backend.services.providers.anthropic import AnthropicProvider
        return AnthropicProvider()

    # Unknown provider — fail loudly at startup, not silently at request time
    raise ValueError(
        f"Unknown LLM_PROVIDER: '{provider_name}'. "
        "Supported values: ollama, anthropic"
    )
