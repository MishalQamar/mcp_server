from fastmcp import FastMCP

from .config.settings import settings
from .routers.prompts import register_mcp_prompts
from .routers.resources import register_mcp_resources
from .routers.tools import register_mcp_tools
from .utils.logging_utils import configure_logging


configure_logging()


def create_mcp_server() -> FastMCP:
    """Create and configure the FastMCP server instance."""
    mcp = FastMCP(
        name=settings.server_name,
        version=settings.version,
    )

    register_mcp_prompts(mcp)
    register_mcp_resources(mcp)
    register_mcp_tools(mcp)

    return mcp


mcp = create_mcp_server()


if __name__ == "__main__":
    mcp.run()
