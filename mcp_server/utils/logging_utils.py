import logging
from rich.logging import RichHandler

from ..config.settings import settings


def configure_logging() -> None:
    """Configure application-wide logging."""

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
