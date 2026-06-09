"""Application configuration using pydantic-settings."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    APP_NAME: str = "KnowledgeReader"
    ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    SECRET_KEY: str = "change-this-secret-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "reader"
    MYSQL_PASSWORD: str = "reader_pass"
    MYSQL_DATABASE: str = "knowledge_reader"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "knowledge-reader"
    MINIO_SECURE: bool = False

    # CORS
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> Any:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
            if normalized in {"debug", "dev", "development"}:
                return True
        return value

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    @property
    def MINIO_CLIENT_CONFIG(self) -> dict:
        return {
            "endpoint": self.MINIO_ENDPOINT,
            "access_key": self.MINIO_ACCESS_KEY,
            "secret_key": self.MINIO_SECRET_KEY,
            "secure": self.MINIO_SECURE,
        }


settings = Settings()
