from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    APP_NAME: str = "real-estate-lead-bot"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/real_estate_leads"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/real_estate_leads"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook"
    N8N_WEBHOOK_SECRET: str = ""

    AI_API_KEY: str = ""
    AI_BASE_URL: str = ""
    AI_MODEL: str = "gpt-4o-mini"
    AI_TIMEOUT_SECONDS: int = 30

    LOG_LEVEL: str = "INFO"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
