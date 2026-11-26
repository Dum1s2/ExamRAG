"""Тесты конфигурации приложения."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from examrag.config import Settings

ENV_KEYS = (
    "LLM_PROVIDER",
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "OPENAI_COMPAT_BASE_URL",
    "OPENAI_COMPAT_API_KEY",
    "OLLAMA_BASE_URL",
    "EMBEDDING_MODEL",
    "DATA_DIR",
    "DATABASE_URL",
)


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет значения по умолчанию без .env и переменных окружения."""
    for key in ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    settings = Settings(_env_file=None)

    assert settings.llm_provider == "gemini"
    assert settings.gemini_api_key is None
    assert settings.gemini_model == ""
    assert settings.openai_compat_base_url is None
    assert settings.openai_compat_api_key is None
    assert settings.ollama_base_url == "http://localhost:11434"
    assert settings.embedding_model == "intfloat/multilingual-e5-small"
    assert settings.data_dir == Path("data")
    assert settings.database_url == "sqlite:///data/examrag.db"


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет переопределение провайдера через переменную окружения."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")

    settings = Settings(_env_file=None)

    assert settings.llm_provider == "ollama"


def test_settings_secret_masking() -> None:
    """Проверяет, что API-ключ в SecretStr не утекает в repr."""
    settings = Settings(gemini_api_key=SecretStr("sk-test-123"), _env_file=None)

    assert "sk-test-123" not in repr(settings)
    assert settings.gemini_api_key is not None
    assert settings.gemini_api_key.get_secret_value() == "sk-test-123"
