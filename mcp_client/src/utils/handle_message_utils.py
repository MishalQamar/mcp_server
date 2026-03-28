from fastmcp import Client
from rich import print

from .command_utils import handle_command
from .handle_agent_loop_utils import handle_agent_loop
from .print_utils import print_header
from .types import InputType, ProcessedInput


async def handle_user_message(
    processed_input: ProcessedInput,
    tools,
    resources,
    prompts,
    conversation_history: list,
    mcp_client: Client,
    thinking_enabled: bool = True,
):
    """
    Route a parsed user input to the correct handler.

    Depending on input_type, this may:
    - print tool/resource/prompt info
    - load a server-hosted prompt
    - fetch a resource
    - run the agent loop for normal messages
    """

    if processed_input.input_type in {
        InputType.COMMAND_INFO_TOOLS,
        InputType.COMMAND_INFO_RESOURCES,
        InputType.COMMAND_INFO_PROMPTS,
    }:
        handle_command(processed_input, tools, resources, prompts)
        return

    if processed_input.input_type == InputType.COMMAND_PROMPT:
        prompt_name = processed_input.prompt_name
        if not prompt_name:
            print("[red]No prompt name provided.[/red]")
            return

        prompt_result = await mcp_client.get_prompt(prompt_name)
        print_header(f"💬 Loaded Prompt: {prompt_name}")

        prompt_text = ""
        if getattr(prompt_result, "messages", None):
            first_message = prompt_result.messages[0]
            if hasattr(first_message, "content") and hasattr(
                first_message.content, "text"
            ):
                prompt_text = first_message.content.text
            else:
                prompt_text = str(first_message)
        else:
            prompt_text = str(prompt_result)

        print(prompt_text)
        conversation_history.append(
            {
                "role": "user",
                "content": prompt_text,
            }
        )
        return

    if processed_input.input_type == InputType.COMMAND_RESOURCE:
        resource_uri = processed_input.resource_uri
        if not resource_uri:
            print("[red]No resource URI provided.[/red]")
            return

        resource_result = await mcp_client.read_resource(resource_uri)
        print_header(f"📚 Resource: {resource_uri}")

        if resource_result and hasattr(resource_result[0], "text"):
            print(resource_result[0].text)
        else:
            print(str(resource_result))
        return

    if processed_input.input_type == InputType.UNKNOWN_COMMAND:
        print("[red]Unknown command.[/red]")
        return

    if processed_input.input_type == InputType.NORMAL_MESSAGE:
        conversation_history.append(
            {
                "role": "user",
                "content": processed_input.raw_text,
            }
        )

        await handle_agent_loop(
            conversation_history=conversation_history,
            tools=tools,
            client=mcp_client,
            thinking_enabled=thinking_enabled,
        )
        return
