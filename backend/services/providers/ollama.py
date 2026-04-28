"""
Ollama provider — talks to a locally running Ollama server.

No API key required. Runs entirely on your machine.
Ollama API docs: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import os
import httpx
from typing import List, Dict
from backend.services.providers.base import BaseProvider

CHAT_TIMEOUT = 180.0   # Ollama can be slow loading a model for the first time
HEALTH_TIMEOUT = 3.0


class OllamaProvider(BaseProvider):
    """
    Calls the local Ollama server at /api/chat.
    Uses stream=false to get a single complete JSON response.
    """

    def __init__(self) -> None:
        self._base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
        self._model    = os.getenv("OLLAMA_MODEL", "llama3")

    @property
    def model(self) -> str:
        return self._model

    @property
    def provider_name(self) -> str:
        return "ollama"

    def is_reachable(self) -> bool:
        """Ping the Ollama root endpoint. Fast — no model involved."""
        try:
            with httpx.Client(timeout=HEALTH_TIMEOUT) as client:
                r = client.get(self._base_url)
                return r.status_code == 200
        except Exception:
            return False

    def chat(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
    ) -> str:
        """
        POST to /api/chat with stream=false.
        Prepends the system prompt as a system-role message.
        """
        endpoint = f"{self._base_url}/api/chat"

        # Ollama accepts system as a role in the messages array
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        payload = {
            "model":    self._model,
            "messages": full_messages,
            "stream":   False,
        }

        try:
            with httpx.Client(timeout=CHAT_TIMEOUT) as client:
                response = client.post(endpoint, json=payload)
        except httpx.ConnectError:
            raise RuntimeError(
                f"Cannot connect to Ollama at {self._base_url}. "
                "Make sure Ollama is running: ollama serve"
            )
        except httpx.TimeoutException:
            raise RuntimeError(
                f"Ollama request timed out after {CHAT_TIMEOUT}s. "
                "The model may still be loading — try again in a moment."
            )

        if response.status_code != 200:
            try:
                detail = response.json().get("error", response.text)
            except Exception:
                detail = response.text

            if "model" in detail.lower() and (
                "not found" in detail.lower() or "pull" in detail.lower()
            ):
                raise RuntimeError(
                    f"Model '{self._model}' is not installed. "
                    f"Run: ollama pull {self._model}"
                )
            raise RuntimeError(f"Ollama error {response.status_code}: {detail}")

        data = response.json()
        content = data.get("message", {}).get("content", "")

        if not content:
            raise RuntimeError("Ollama returned an empty response.")

        return content
