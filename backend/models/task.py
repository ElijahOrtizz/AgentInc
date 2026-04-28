"""
Pydantic models for request/response validation.
Keeping these in one file makes it easy to see the full API contract at a glance.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ConversationMessage(BaseModel):
    """Single turn in a conversation history."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """
    Incoming chat request from the frontend.
    agent_id maps to a system prompt on the backend.
    conversation holds prior turns so the model has context.
    auto_route controls whether we run the task classifier.
    """
    agent_id: str = Field(..., description="Which agent to use (ops, general, stryde, etc.)")
    message: str = Field(..., description="The user's latest message")
    conversation: List[ConversationMessage] = Field(
        default_factory=list,
        description="Prior conversation turns for context"
    )
    auto_route: bool = Field(default=True, description="Whether to classify and return routing info")


class RoutingResult(BaseModel):
    """
    Result from the task classifier.
    Mirrors what the frontend JS classifier was producing.
    """
    task_type: str
    workflow: str           # "claude", "chatgpt", or "general"
    workflow_label: str     # Human-readable label shown in the UI
    reason: str


class ChatResponse(BaseModel):
    """
    Response sent back to the frontend.
    reply is the assistant's text.
    routing is optional — only populated when auto_route=True.
    """
    reply: str
    routing: Optional[RoutingResult] = None


class ErrorResponse(BaseModel):
    """Standard error shape for all failure cases."""
    error: str
    detail: Optional[str] = None
