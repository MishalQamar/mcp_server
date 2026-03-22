import json
from pathlib import Path
from typing import Any

from ..app.guideline_extractions_handler import extract_local_paths, extract_urls
from ..config.constants import (
    ARTICLE_GUIDELINE_FILE,
    GUIDELINES_FILENAMES_FILE,
    NOVA_FOLDER,
)
from ..utils.file_utils import read_file_safe


def extract_guidelines_urls_tool(research_directory: str) -> dict[str, Any]:
    """
    Extract URLs and local file references from the article guideline file.

    Reads article_guideline.md from the research directory, extracts GitHub URLs,
    YouTube URLs, other URLs, and local file references, then saves the result to
    .nova/guidelines_filenames.json.
    """
    research_path = Path(research_directory)
    nova_path = research_path / NOVA_FOLDER
    guidelines_path = research_path / ARTICLE_GUIDELINE_FILE

    if not guidelines_path.exists():
        raise FileNotFoundError(
            f"Guideline file not found: {guidelines_path.resolve()}"
        )

    nova_path.mkdir(parents=True, exist_ok=True)

    guidelines_content = read_file_safe(guidelines_path)

    all_urls = extract_urls(guidelines_content)
    github_urls = [u for u in all_urls if "github.com" in u]
    youtube_urls = [u for u in all_urls if "youtube.com" in u or "youtu.be" in u]
    other_urls = [
        u
        for u in all_urls
        if "github.com" not in u and "youtube.com" not in u and "youtu.be" not in u
    ]

    local_file_paths = extract_local_paths(guidelines_content)

    extracted_data = {
        "github_urls": github_urls,
        "youtube_videos_urls": youtube_urls,
        "other_urls": other_urls,
        "local_file_paths": local_file_paths,
    }

    output_path = nova_path / GUIDELINES_FILENAMES_FILE
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "github_sources_count": len(github_urls),
        "youtube_sources_count": len(youtube_urls),
        "web_sources_count": len(other_urls),
        "local_files_count": len(local_file_paths),
        "output_path": str(output_path.resolve()),
        "message": (
            f"Successfully extracted URLs from article guidelines in "
            f"'{research_directory}'. Found {len(github_urls)} GitHub URLs, "
            f"{len(youtube_urls)} YouTube URLs, {len(other_urls)} other URLs, "
            f"and {len(local_file_paths)} local file references."
        ),
    }
