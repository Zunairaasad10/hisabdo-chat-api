from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HisabDo AI Business Assistant"
    groq_api_key: str | None = None
    groq_model: str = "openai/gpt-oss-20b"
    max_history_messages: int = 12
    log_file: str = "logs/chat.jsonl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()