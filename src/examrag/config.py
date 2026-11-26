"""Конфигурация приложения на базе pydantic-settings."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки ExamRAG, считываемые из переменных окружения и файла .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: Literal["gemini", "openai_compat", "ollama"] = "gemini"
    # SecretStr не печатается в логах и repr()
    gemini_api_key: SecretStr | None = None
    gemini_model: str = ""
    openai_compat_base_url: str | None = None
    openai_compat_api_key: SecretStr | None = None
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "intfloat/multilingual-e5-small"
    data_dir: Path = Path("data")
    database_url: str = "sqlite:///data/examrag.db"


@lru_cache
def get_settings() -> Settings:
    """Возвращает кэшированный экземпляр настроек приложения."""
    return Settings()
