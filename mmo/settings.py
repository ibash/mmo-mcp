import typing as T

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    anthropic_api_key: str
    # Persistence mode: "disk" for local JSON files, "postgres" for PostgreSQL
    persist_mode: T.Literal["disk", "postgres"] = "disk"
    database_url: PostgresDsn | None = None


settings = Settings()  # type: ignore
