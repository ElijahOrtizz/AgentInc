"""
Chat route — unchanged in structure, now provider-agnostic.

The only change from the original: call_anthropic() is replaced by
get_provider().chat(), which routes to whichever provider is configured
in LLM_PROVIDER. Everything else stays the same.
"""

from fastapi import APIRouter, HTTPException
from backend.models.task import ChatRequest, ChatResponse, RoutingResult
from backend.services.provider_factory import get_provider
from backend.services.agent_prompts import get_prompt
from backend.services.router import classify_task

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Handle a chat turn from the frontend.
    Accepts the full conversation history for context.
    Returns the assistant reply plus optional routing classification.
    """

    # 1. Get system prompt for this agent (owned by backend, not frontend)
    system_prompt = get_prompt(request.agent_id)

    # 2. Build full message history
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in request.conversation
    ]
    messages.append({"role": "user", "content": request.message})

    # 3. Classify task if auto_route is enabled
    routing: RoutingResult | None = None
    if request.auto_route:
        routing = classify_task(request.message)

    # 4. Call the active provider — Ollama, Anthropic, or whatever is configured
    provider = get_provider()
    try:
        reply = provider.chat(system_prompt=system_prompt, messages=messages)

    except RuntimeError as e:
        # Provider-level errors: offline, model not installed, API key missing, etc.
        raise HTTPException(status_code=502, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected backend error: {str(e)}"
        )

    return ChatResponse(reply=reply, routing=routing)
