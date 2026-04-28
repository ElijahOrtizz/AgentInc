"""
Health check route.
Now reports the active provider, model, and reachability so the frontend
status badge shows accurate, useful information regardless of which provider
is configured.
"""

import os
from fastapi import APIRouter
from backend.services.provider_factory import get_provider

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Returns backend status plus provider info.

    Response shape:
    {
        "status": "ok",
        "service": "agent-ops-backend",
        "provider": "ollama",
        "model": "llama3",
        "provider_reachable": true,
        "api_key_configured": false
    }

    Frontend uses this to display:
      Green  + "Connected · llama3"         → provider_reachable = true
      Yellow + "Ollama offline"              → ollama selected but not reachable
      Yellow + "Anthropic: no API key"       → anthropic selected, key missing
      Red    + "Backend offline"             → FastAPI itself unreachable
    """
    try:
        provider = get_provider()
        reachable = provider.is_reachable()
        provider_name = provider.provider_name
        model = provider.model
    except ValueError as e:
        # Bad LLM_PROVIDER value in .env — surface clearly
        return {
            "status":            "error",
            "service":           "agent-ops-backend",
            "provider":          os.getenv("LLM_PROVIDER", "unknown"),
            "model":             "unknown",
            "provider_reachable": False,
            "api_key_configured": False,
            "error":             str(e),
        }

    return {
        "status":             "ok",
        "service":            "agent-ops-backend",
        "provider":           provider_name,
        "model":              model,
        "provider_reachable": reachable,
        # Only meaningful for Anthropic; always False for Ollama (no key needed)
        "api_key_configured": bool(os.getenv("ANTHROPIC_API_KEY", "")),
    }
