from pathlib import Path
from typing import Any

from ..app.generate_queries_handler import generate_queries_with_reasons
from ..app.query_file_handler import write_queries_to_file
from ..config.constants import (
    ARTICLE_GUIDELINE_FILE,
    MARKDOWN_EXTENSION,
    NEXT_QUERIES_FILE,
    NOVA_FOLDER,
    PERPLEXITY_RESULTS_FILE,
    URLS_FROM_GUIDELINES_FOLDER,
)
from ..utils.file_utils import read_file_safe


async def generate_next_queries_tool(
    research_directory: str,
    n_queries: int = 5,
) -> dict[str, Any]:
    """
    Generate candidate web-search queries for the next research round.

    Uses:
    - article guidelines
    - existing Perplexity research results
    - already-scraped guideline URLs

    Saves the result to:
    .nova/next_queries.md
    """
    research_path = Path(research_directory)
    nova_path = research_path / NOVA_FOLDER

    guidelines_path = research_path / ARTICLE_GUIDELINE_FILE
    results_path = nova_path / PERPLEXITY_RESULTS_FILE
    urls_from_guidelines_dir = nova_path / URLS_FROM_GUIDELINES_FOLDER

    article_guidelines = ""
    if guidelines_path.exists():
        article_guidelines = read_file_safe(guidelines_path)

    past_research = ""
    if results_path.exists():
        past_research = read_file_safe(results_path)

    scraped_ctx_parts: list[str] = []
    if urls_from_guidelines_dir.exists():
        for md_file in sorted(urls_from_guidelines_dir.glob(f"*{MARKDOWN_EXTENSION}")):
            scraped_ctx_parts.append(md_file.read_text(encoding="utf-8"))

    scraped_ctx_str = "\n\n".join(scraped_ctx_parts)

    queries_and_reasons = await generate_queries_with_reasons(
        article_guidelines=article_guidelines,
        past_research=past_research,
        scraped_ctx=scraped_ctx_str,
        n_queries=n_queries,
    )

    next_q_path = nova_path / NEXT_QUERIES_FILE
    write_queries_to_file(next_q_path, queries_and_reasons)

    return {
        "status": "success",
        "queries_count": len(queries_and_reasons),
        "queries": queries_and_reasons,
        "output_path": str(next_q_path.resolve()),
        "message": (
            f"Successfully generated {len(queries_and_reasons)} candidate queries "
            f"for research folder '{research_directory}'. "
            f"Saved to: {next_q_path.resolve()}"
        ),
    }
