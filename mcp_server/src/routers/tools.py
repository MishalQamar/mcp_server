from typing import Any

from fastmcp import FastMCP

from ..tools.extract_guidelines_urls_tool import extract_guidelines_urls_tool
from ..tools.generate_next_queries_tool import generate_next_queries_tool
from ..tools.process_github_urls_tool import process_github_urls_tool
from ..tools.process_local_files_tool import process_local_files_tool
from ..tools.scrape_and_clean_other_urls_tool import (
    scrape_and_clean_other_urls_tool,
)
from ..tools.transcribe_youtube_videos_tool import (
    transcribe_youtube_videos_tool,
)


def register_mcp_tools(mcp: FastMCP) -> None:
    """Register all MCP tools with the server instance."""

    @mcp.tool(
        name="extract_guidelines_urls",
        description="Extract URLs and local file references from article guidelines.",
    )
    async def extract_guidelines_urls(research_directory: str) -> dict[str, Any]:
        """Extract URLs and local file references from article guidelines."""
        return extract_guidelines_urls_tool(research_directory=research_directory)

    @mcp.tool(
        name="process_local_files",
        description="Process local files referenced in the extracted guidelines metadata.",
    )
    async def process_local_files(research_directory: str) -> dict[str, Any]:
        """Process local files referenced in the article guidelines."""
        return process_local_files_tool(research_directory=research_directory)

    @mcp.tool(
        name="scrape_and_clean_other_urls",
        description="Scrape and clean the non-GitHub, non-YouTube URLs from the extracted guidelines metadata.",
    )
    async def scrape_and_clean_other_urls(
        research_directory: str,
        concurrency_limit: int = 4,
    ) -> dict[str, Any]:
        """Scrape and clean the 'other_urls' found in the article guidelines metadata."""
        return await scrape_and_clean_other_urls_tool(
            research_directory=research_directory,
            concurrency_limit=concurrency_limit,
        )

    @mcp.tool(
        name="process_github_urls",
        description="Process GitHub URLs from the extracted guidelines metadata into LLM-friendly markdown digests.",
    )
    async def process_github_urls(research_directory: str) -> dict[str, Any]:
        """Process GitHub URLs referenced in the article guidelines."""
        return await process_github_urls_tool(research_directory=research_directory)

    @mcp.tool(
        name="transcribe_youtube_urls",
        description="Transcribe YouTube video URLs from the extracted guidelines metadata into markdown transcripts.",
    )
    async def transcribe_youtube_urls(research_directory: str) -> dict[str, Any]:
        """Transcribe YouTube videos referenced in the article guidelines."""
        return await transcribe_youtube_videos_tool(
            research_directory=research_directory
        )

    @mcp.tool(
        name="generate_next_queries",
        description="Analyze the current research context and generate the next set of web-search queries with reasons.",
    )
    async def generate_next_queries(
        research_directory: str,
        n_queries: int = 5,
    ) -> dict[str, Any]:
        """Generate the next candidate research queries from existing context."""
        return await generate_next_queries_tool(
            research_directory=research_directory,
            n_queries=n_queries,
        )
