"""
Agent Ops Backend — FastAPI entry point.
Provider-abstracted: supports Ollama (default, free) and Anthropic.
Set LLM_PROVIDER in .env to switch providers.

Run with:
    uvicorn backend.main:app --reload --port 8000
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Must load before any route imports that call os.getenv()
load_dotenv()

from backend.routes.health import router as health_router
from backend.routes.chat   import router as chat_router

app = FastAPI(
    title="Agent Ops Backend",
    description="AI Operations Cockpit — multi-provider LLM backend",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(chat_router)


@app.on_event("startup")
async def startup_check():
    """Print a clear startup summary so you know exactly what the server is using."""
    from backend.services.provider_factory import get_provider

    print("\n" + "=" * 56)
    print("  Agent Ops Backend  v3.0")
    print("=" * 56)

    try:
        provider  = get_provider()
        reachable = provider.is_reachable()

        print(f"  Provider : {provider.provider_name}")
        print(f"  Model    : {provider.model}")
        print(f"  Ready    : {'YES' if reachable else 'NO'}")

        if not reachable:
            print()
            if provider.provider_name == "ollama":
                print("  Ollama is not reachable.")
                print("  Start it:   ollama serve")
                print(f"  Pull model: ollama pull {provider.model}")
            elif provider.provider_name == "anthropic":
                print("  Anthropic API key not configured.")
                print("  Add ANTHROPIC_API_KEY to your .env file.")

    except ValueError as e:
        print(f"  CONFIG ERROR: {e}")

    print("=" * 56 + "\n")


@app.get("/")
def root():
    return {
        "message": "Agent Ops Backend is running.",
        "docs":    "http://127.0.0.1:8000/docs",
        "health":  "http://127.0.0.1:8000/health",
    }
