from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10000)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=10000)
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    model: str
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    llm_configured: bool
