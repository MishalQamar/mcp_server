from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for the MCP server."""

    # =========================
    # General Server Info
    # =========================
    app_name: str = "Research Agent MCP Server"
    app_version: str = "0.1.0"

    # =========================
    # LLM Models
    # =========================

    # Used later for query generation, source selection, etc.
    default_model: str = "gemini-2.0-flash"

    # Used specifically for YouTube transcription (multimodal)
    youtube_transcription_model: str = "gemini-2.0-flash"

    # =========================
    # API Keys (optional now)
    # =========================
    google_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance used across the app
settings = Settings()
