from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the MCP server."""

    server_name: str = "Research Agent"
    version: str = "0.1.0"

    log_level: str = "INFO"

    opik_api_key: str | None = None
    opik_workspace: str | None = None
    opik_project_name: str = "nova-research-agent"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
