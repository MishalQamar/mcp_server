import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from ..app.youtube_handler import transcribe_youtube
from ..config.constants import (
    GUIDELINES_FILENAMES_FILE,
    NOVA_FOLDER,
    URLS_FROM_GUIDELINES_YOUTUBE_FOLDER,
)
from ..utils.file_utils import read_file_safe


def youtube_url_to_filename(url: str) -> str:
    """
    Convert a YouTube URL into a safe markdown filename.
    """
    parsed = urlparse(url)
    base = f"{parsed.netloc}{parsed.path}{parsed.query}"

    if not base:
        base = "youtube-video"

    base = base.replace("/", "-").replace("?", "-").replace("&", "-").replace("=", "-")
    base = re.sub(r"[^a-zA-Z0-9._-]+", "-", base)
    base = re.sub(r"-{2,}", "-", base).strip("-")

    if not base.endswith(".md"):
        base += ".md"

    return base.lower()


async def transcribe_youtube_videos_tool(research_directory: str) -> dict[str, Any]:
    """
    Transcribe YouTube video URLs from .nova/guidelines_filenames.json.

    Reads the 'youtube_videos_urls' list, transcribes each public video
    into markdown, and saves the results into:
    .nova/urls_from_guidelines_youtube_videos/
    """
    research_path = Path(research_directory)
    nova_path = research_path / NOVA_FOLDER
    metadata_path = nova_path / GUIDELINES_FILENAMES_FILE
    output_dir = nova_path / URLS_FROM_GUIDELINES_YOUTUBE_FOLDER

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Guidelines metadata file not found: {metadata_path.resolve()}"
        )

    data = json.loads(read_file_safe(metadata_path))
    youtube_urls = data.get("youtube_videos_urls", [])

    output_dir.mkdir(parents=True, exist_ok=True)

    if not youtube_urls:
        return {
            "status": "success",
            "urls_processed": 0,
            "urls_total": 0,
            "files_saved": 0,
            "saved_files": [],
            "output_directory": str(output_dir.resolve()),
            "message": "No YouTube URLs found to process in the guidelines metadata file.",
        }

    saved_files: list[str] = []
    processed_count = 0
    errors: list[str] = []

    for url in youtube_urls:
        filename = youtube_url_to_filename(url)
        output_path = output_dir / filename

        try:
            await transcribe_youtube(
                url=url,
                output_path=output_path,
                timestamp=30,
            )
            saved_files.append(filename)
            processed_count += 1

        except Exception as e:
            errors.append(f"Failed to transcribe {url}: {str(e)}")

    return {
        "status": "success" if processed_count > 0 else "warning",
        "urls_processed": processed_count,
        "urls_total": len(youtube_urls),
        "files_saved": len(saved_files),
        "saved_files": saved_files,
        "errors": errors,
        "output_directory": str(output_dir.resolve()),
        "message": (
            f"Processed {processed_count}/{len(youtube_urls)} YouTube URLs from "
            f"guidelines metadata in '{research_directory}'. "
            f"Saved transcripts to: {output_dir.resolve()}"
        ),
    }
