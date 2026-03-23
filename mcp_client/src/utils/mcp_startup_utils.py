from fastmcp import Client


async def get_capabilities_from_mcp_client(mcp_client: Client):
    """
    Fetch tools, resources, and prompts from the connected MCP server.

    Returns:
        A tuple of (tools, resources, prompts).
    """
    tools = await mcp_client.list_tools()
    resources = await mcp_client.list_resources()
    prompts = await mcp_client.list_prompts()

    return tools, resources, prompts
