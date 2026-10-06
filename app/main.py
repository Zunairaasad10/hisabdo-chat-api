from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from .config import settings
from .logging_utils import configure_logging, log_chat
from .llm import LLMNotConfiguredError, GroqChatService
from .models import ChatMessage, ChatRequest, ChatResponse, HealthResponse
from .session_store import InMemorySessionStore


configure_logging()

app = FastAPI(title=settings.app_name, version="0.1.0")

sessions = InMemorySessionStore(
    max_messages=settings.max_history_messages
)

llm = GroqChatService()


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        llm_configured=llm.client is not None
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Request-provided history is useful for clients migrating an existing chat.
    history = (
        request.history
        if request.history is not None
        else sessions.get(request.session_id)
    )

    try:
        answer = llm.generate(
            history,
            request.message
        )

    except LLMNotConfiguredError as exc:
        log_chat(
            session_id=request.session_id,
            status="error",
            error="llm_not_configured"
        )

        raise HTTPException(
            status_code=503,
            detail="LLM is not configured. Set GROQ_API_KEY."
        ) from exc

    except Exception as exc:
        log_chat(
            session_id=request.session_id,
            status="error",
            error=type(exc).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="The LLM service could not generate a response."
        ) from exc

    sessions.append(
        request.session_id,
        ChatMessage(
            role="user",
            content=request.message
        )
    )

    sessions.append(
        request.session_id,
        ChatMessage(
            role="assistant",
            content=answer
        )
    )

    response = ChatResponse(
        session_id=request.session_id,
        message=answer,
        model=settings.groq_model,
        timestamp=datetime.now(timezone.utc),
    )

    log_chat(
        session_id=request.session_id,
        status="success",
        user_message=request.message,
        response=answer,
        model=settings.groq_model,
    )

    return response