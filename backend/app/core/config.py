from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    APP_NAME: str = "real-estate-lead-bot"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    DATABASE_URL: str = "mysql+aiomysql://root:1234@localhost:3306/real_estate_leads"
    DATABASE_URL_SYNC: str = "mysql+pymysql://root:1234@localhost:3306/real_estate_leads"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    N8N_WEBHOOK_URL: str = "http://127.0.0.1:5678/webhook/primehomes/lead/process-message"
    N8N_WEBHOOK_SECRET: str = ""
    N8N_CONTEXT_MESSAGE_LIMIT: int = 12

    AI_API_KEY: str = ""
    AI_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    AI_MODEL: str = "openai/gpt-oss-120b"
    AI_TIMEOUT_SECONDS: int = 30

    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    LLM_MODEL: str = "openai/gpt-oss-120b"

    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    LOG_LEVEL: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
