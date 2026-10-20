"""All runtime configuration, read from environment variables / .env.

One typed object instead of os.getenv() scattered around the code: typos fail
at startup, and every knob the system has is visible in one place.
"""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    database_url: str = "postgresql://paragraf:paragraf@localhost:5432/paragraf"

    llm_provider: Literal["groq", "openai", "anthropic"] = "groq"
    llm_model: str = "llama-3.1-8b-instant"
    judge_model: str = "llama-3.3-70b-versatile"
    # SecretStr keeps keys out of repr() and therefore out of logs and tracebacks.
    groq_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None

    embedding_model: str = "BAAI/bge-m3"

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
