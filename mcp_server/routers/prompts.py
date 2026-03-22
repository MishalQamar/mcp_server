from fastmcp import FastMCP

from ..prompts.research_instructions_prompt import (
    full_research_instructions_prompt as _get_research_instructions,
)


def register_mcp_prompts(mcp: FastMCP) -> None:
    """Register all mcp prompts for the server instance."""

    @mcp.prompt("full_research_instructions")
    def full_research_instructions_prompt() -> str:
        """The main prompt that drives the research agent workflow."""

        return _get_research_instructions()
