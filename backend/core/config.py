# backend/core/config.py
from pydantic_settings import BaseSettings
from typing import list


class Settings(BaseSettings):
    DATABASE_URL:    str = "postgresql+asyncpg://openblog:changeme@localhost/openblog"
    REDIS_URL:       str = "redis://localhost:6379"
    JWT_SECRET:      str = "change-me-in-production"
    JWT_EXPIRE_DAYS: int = 7

    S3_BUCKET:       str = "openblog-media"
    S3_REGION:       str = "us-east-1"
    S3_ENDPOINT_URL: str = ""  # Set for non-AWS S3-compatible storage

    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
