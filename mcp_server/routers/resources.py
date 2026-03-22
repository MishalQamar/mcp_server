from fastmcp import FastMCP

from ..resources.system_resources import get_memory_resource


def register_mcp_resources(mcp: FastMCP) -> None:
    """Register all MCP resources with the server instance."""

    @mcp.resource("system://memory")
    async def system_memory() -> dict:
        """Returns memory usage statistics."""
        return await get_memory_resource()
