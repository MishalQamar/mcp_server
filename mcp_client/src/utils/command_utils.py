from .print_utils import Color, print_header, print_item
from .types import InputType, ProcessedInput


def handle_command(processed_input: ProcessedInput, tools, resources, prompts) -> None:
    """
    Handle informational commands.

    This function only handles the simple info commands:
    - /tools
    - /resources
    - /prompts
    """
    if processed_input.input_type == InputType.COMMAND_INFO_TOOLS:
        print_header("🛠️ Available Tools")
        for i, tool in enumerate(tools, 1):
            print_item(
                name=tool.name,
                description=getattr(tool, "description", None),
                index=i,
                name_color=Color.BRIGHT_WHITE,
                index_color=Color.YELLOW,
            )
        return

    if processed_input.input_type == InputType.COMMAND_INFO_RESOURCES:
        print_header("📚 Available Resources")
        for i, resource in enumerate(resources, 1):
            print_item(
                name=str(resource.uri),
                description=getattr(resource, "description", None),
                index=i,
                name_color=Color.BRIGHT_WHITE,
                index_color=Color.YELLOW,
            )
        return

    if processed_input.input_type == InputType.COMMAND_INFO_PROMPTS:
        print_header("💬 Available Prompts")
        for i, prompt in enumerate(prompts, 1):
            print_item(
                name=prompt.name,
                description=getattr(prompt, "description", None),
                index=i,
                name_color=Color.BRIGHT_WHITE,
                index_color=Color.YELLOW,
            )
        return
