try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .config import settings
from .models import ChatMessage
from .prompts import HISABDO_SYSTEM_PROMPT


class LLMNotConfiguredError(RuntimeError):
    pass


class GroqChatService:
    def __init__(self):
        self.client = (
            OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1",
            )
            if (settings.groq_api_key and OpenAI is not None)
            else None
        )

    def generate(self, history: list[ChatMessage], user_message: str) -> str:
        if self.client is None:
            raise LLMNotConfiguredError("GROQ_API_KEY is not configured")

        input_items = [
            {"role": item.role, "content": item.content}
            for item in history
        ]

        input_items.append(
            {"role": "user", "content": user_message}
        )

        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": HISABDO_SYSTEM_PROMPT,
                },
                *input_items,
            ],
        )

        return response.choices[0].message.content.strip()