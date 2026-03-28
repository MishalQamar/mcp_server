import json
from pathlib import Path
from typing import Any

from ..app.scraping_handler import (
    scrape_urls_concurrently,
    write_scraped_results_to_files,
)
from ..config.constants import (
    ARTICLE_GUIDELINE_FILE,
    GUIDELINES_FILENAMES_FILE,
    NOVA_FOLDER,
    URLS_FROM_GUIDELINES_FOLDER,
)
from ..utils.file_utils import read_file_safe


async def scrape_and_clean_other_urls_tool(
    research_directory: str,
    concurrency_limit: int = 4,
) -> dict[str, Any]:
    """
    Scrape and clean the 'other_urls' listed in .nova/guidelines_filenames.json.

    Saves cleaned markdown files into:
    .nova/urls_from_guidelines/
    """
    research_path = Path(research_directory)
    nova_path = research_path / NOVA_FOLDER
    guidelines_file_path = nova_path / GUIDELINES_FILENAMES_FILE

    if not guidelines_file_path.exists():
        raise FileNotFoundError(
            f"Guidelines metadata file not found: {guidelines_file_path.resolve()}"
        )

    guidelines_data = json.loads(read_file_safe(guidelines_file_path))
    urls_to_scrape = guidelines_data.get("other_urls", [])

    output_dir = nova_path / URLS_FROM_GUIDELINES_FOLDER

    if not urls_to_scrape:
        output_dir.mkdir(parents=True, exist_ok=True)
        return {
            "status": "success",
            "urls_processed": [],
            "urls_failed": [],
            "total_urls": 0,
            "successful_urls_count": 0,
            "failed_urls_count": 0,
            "output_directory": str(output_dir.resolve()),
            "message": "No other URLs found to scrape in the guidelines metadata file.",
        }

    guidelines_path = research_path / ARTICLE_GUIDELINE_FILE
    article_guidelines = ""
    if guidelines_path.exists():
        article_guidelines = read_file_safe(guidelines_path)

    completed_results = await scrape_urls_concurrently(
        urls=urls_to_scrape,
        concurrency_limit=concurrency_limit,
        article_guidelines=article_guidelines,
    )

    saved_files, successful_scrapes = write_scraped_results_to_files(
        completed_results=completed_results,
        output_dir=output_dir,
    )

    failed_urls = [
        result["url"]
        for result in completed_results
        if not result.get("success", False)
    ]
    successful_urls = [
        result["url"] for result in completed_results if result.get("success", False)
    ]

    return {
        "status": "success",
        "urls_processed": successful_urls,
        "urls_failed": failed_urls,
        "total_urls": len(urls_to_scrape),
        "successful_urls_count": successful_scrapes,
        "failed_urls_count": len(failed_urls),
        "saved_files": saved_files,
        "output_directory": str(output_dir.resolve()),
        "message": (
            f"Successfully processed {successful_scrapes}/{len(urls_to_scrape)} URLs. "
            f"Results saved to: {output_dir.resolve()}"
        ),
    }
