from typing import Any

from fastmcp import FastMCP

from ..tools.extract_guidelines_urls_tool import extract_guidelines_urls_tool


def register_mcp_tools(mcp: FastMCP) -> None:
    """Register all MCP tools with the server instance."""

    @mcp.tool(
        name="extract_guidelines_urls",
        description="Extract URLs and local file references from article guidelines.",
    )
    async def extract_guidelines_urls(research_directory: str) -> dict[str, Any]:
        """Extract URLs and local file references from article guidelines."""
        return extract_guidelines_urls_tool(research_directory=research_directory)
