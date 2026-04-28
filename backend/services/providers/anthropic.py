"""
Anthropic provider — optional paid cloud provider.

Only used when LLM_PROVIDER=anthropic in .env.
The backend starts and runs fine without this if the provider is set to ollama.
API key must be set in ANTHROPIC_API_KEY or this provider will raise on chat().
"""

import os
import httpx
from typing import List, Dict
from backend.services.providers.base import BaseProvider

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
CHAT_TIMEOUT      = 120.0
HEALTH_TIMEOUT    = 5.0
DEFAULT_MAX_TOKENS = 4096


class AnthropicProvider(BaseProvider):
    """
    Calls the Anthropic Messages API.
    Requires ANTHROPIC_API_KEY to be set in the environment.
    """

    def __init__(self) -> None:
        self._model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    @property
    def model(self) -> str:
        return self._model

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def _get_key(self) -> str:
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Add it to your .env file or switch LLM_PROVIDER to ollama."
            )
        return key

    def is_reachable(self) -> bool:
        """
        For Anthropic: reachable = API key is configured.
        We don't make a live network call here to avoid costs.
        """
        return bool(os.getenv("ANTHROPIC_API_KEY", ""))

    def chat(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
    ) -> str:
        api_key = self._get_key()

        headers = {
            "Content-Type":    "application/json",
            "x-api-key":       api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        }

        payload = {
            "model":      self._model,
            "max_tokens": DEFAULT_MAX_TOKENS,
            "system":     system_prompt,
            "messages":   messages,
        }

        with httpx.Client(timeout=CHAT_TIMEOUT) as client:
            response = client.post(ANTHROPIC_API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            try:
                detail = response.json().get("error", {}).get("message", response.text)
            except Exception:
                detail = response.text
            raise RuntimeError(f"Anthropic API error {response.status_code}: {detail}")

        data = response.json()
        for block in data.get("content", []):
            if block.get("type") == "text":
                return block["text"]

        raise RuntimeError("Anthropic response contained no text content.")
