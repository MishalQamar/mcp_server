from pathlib import Path


def read_file_safe(path: Path) -> str:
    """Read a UTF-8 text file and return its contents."""
    return path.read_text(encoding="utf-8")
