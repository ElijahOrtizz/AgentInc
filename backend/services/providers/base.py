"""
Base provider interface.

Every LLM provider must implement this interface.
The rest of the backend only talks to this contract — never to a provider directly.
Swapping providers means changing one env var, not touching route logic.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def chat(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
    ) -> str:
        """
        Send a chat request and return the assistant's reply as a plain string.

        Args:
            system_prompt: The agent's system instruction.
            messages:       List of {"role": "user"/"assistant", "content": "..."} dicts.

        Returns:
            Assistant response text.

        Raises:
            RuntimeError: If the provider returns an error or is unreachable.
        """

    @abstractmethod
    def is_reachable(self) -> bool:
        """
        Quick connectivity check used by /health.
        Should be fast (short timeout, no model call).
        Returns True if the provider endpoint is up, False otherwise.
        """

    @property
    @abstractmethod
    def model(self) -> str:
        """Return the model identifier currently in use."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return a short human-readable provider name, e.g. 'ollama' or 'anthropic'."""
