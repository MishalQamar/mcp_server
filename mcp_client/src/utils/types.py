from dataclasses import dataclass
from enum import Enum


class InputType(str, Enum):
    """Supported kinds of user input."""

    NORMAL_MESSAGE = "normal_message"
    COMMAND_INFO_TOOLS = "command_info_tools"
    COMMAND_INFO_RESOURCES = "command_info_resources"
    COMMAND_INFO_PROMPTS = "command_info_prompts"
    COMMAND_PROMPT = "command_prompt"
    COMMAND_RESOURCE = "command_resource"
    COMMAND_QUIT = "command_quit"
    COMMAND_MODEL_THINKING_SWITCH = "command_model_thinking_switch"
    UNKNOWN_COMMAND = "unknown_command"


@dataclass
class ProcessedInput:
    """Structured representation of parsed user input."""

    input_type: InputType
    raw_text: str
    prompt_name: str | None = None
    resource_uri: str | None = None
