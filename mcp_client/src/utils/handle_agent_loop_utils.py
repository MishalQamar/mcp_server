from fastmcp import Client
from rich import print

from ..settings import settings
from .llm_utils import (
    LLMClient,
    build_llm_config_with_tools,
    extract_final_answer,
    extract_first_function_call,
    extract_thought_summary,
)


async def execute_tool(name: str, args: dict, client: Client):
    """Execute a tool through the MCP client and return the raw result."""
    tool_result = await client.call_tool(name, args)
    return tool_result


async def handle_agent_loop(
    conversation_history: list,
    tools: list,
    client: Client,
    thinking_enabled: bool,
):
    """
    Run the agent loop:
    - call the LLM
    - inspect its response
    - execute tools if requested
    - append results back to history
    - stop when a final text answer is produced
    """
    llm_config = build_llm_config_with_tools(
        mcp_tools=tools,
        thinking_enabled=thinking_enabled,
    )
    llm_client = LLMClient(settings.model_id, llm_config)

    while True:
        print()
        response = await llm_client.generate_content(conversation_history)

        if thinking_enabled:
            thoughts = extract_thought_summary(response)
            if thoughts:
                print(f"[bold magenta]🤔 LLM's Thoughts:[/bold magenta]\n{thoughts}")

        function_call_info = extract_first_function_call(response)

        if function_call_info:
            name, args = function_call_info

            is_tool = any(tool.name == name for tool in tools)

            if is_tool:
                print("[bold yellow]🔧 Function Call (Tool):[/bold yellow]")
                print(f"  Tool: [bright_white]{name}[/bright_white]")
                print(f"  Args: [bright_white]{args}[/bright_white]")

                tool_result = await execute_tool(name, args, client)

                # Try to extract readable text from the MCP tool result
                tool_text = ""
                if hasattr(tool_result, "content") and tool_result.content:
                    first_part = tool_result.content[0]
                    tool_text = getattr(first_part, "text", str(first_part))
                else:
                    tool_text = str(tool_result)

                tool_response = (
                    f"Tool '{name}' executed successfully. Result: {tool_text}"
                )

                conversation_history.append(
                    {
                        "role": "user",
                        "content": tool_response,
                    }
                )

                print(f"[green]{tool_response}[/green]")
                continue

        final_text = extract_final_answer(response)
        if final_text:
            conversation_history.append(
                {
                    "role": "model",
                    "content": final_text,
                }
            )
            print(f"[bold cyan]💬 LLM Response:[/bold cyan] {final_text}")
            break

        print("[red]The model returned no tool call and no final answer.[/red]")
        break
