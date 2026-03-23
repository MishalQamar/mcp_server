from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Client configuration settings."""

    # --- Model ---
    model_id: str = "gemini-1.5-pro"

    # --- Thinking ---
    thinking_budget: int = 1024
    thinking_enabled: bool = True

    # --- Transport ---
    transport: str = "in-memory"  # or "stdio"

    # --- Server path (used for stdio mode) ---
    server_main_path: Path = Path("../mcp_server")

    # --- Logging ---
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
