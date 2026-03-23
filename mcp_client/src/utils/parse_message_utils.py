from .types import InputType, ProcessedInput


def parse_user_input(user_input: str) -> ProcessedInput:
    """
    Parse raw user input into a structured ProcessedInput object.
    """

    user_input = user_input.strip()

    # Normal message
    if not user_input.startswith("/"):
        return ProcessedInput(
            input_type=InputType.NORMAL_MESSAGE,
            raw_text=user_input,
        )

    # Informational commands
    if user_input == "/tools":
        return ProcessedInput(
            input_type=InputType.COMMAND_INFO_TOOLS,
            raw_text=user_input,
        )

    if user_input == "/resources":
        return ProcessedInput(
            input_type=InputType.COMMAND_INFO_RESOURCES,
            raw_text=user_input,
        )

    if user_input == "/prompts":
        return ProcessedInput(
            input_type=InputType.COMMAND_INFO_PROMPTS,
            raw_text=user_input,
        )

    if user_input == "/quit":
        return ProcessedInput(
            input_type=InputType.COMMAND_QUIT,
            raw_text=user_input,
        )

    if user_input == "/model-thinking-switch":
        return ProcessedInput(
            input_type=InputType.COMMAND_MODEL_THINKING_SWITCH,
            raw_text=user_input,
        )

    # Prompt loading
    if user_input.startswith("/prompt/"):
        prompt_name = user_input.removeprefix("/prompt/").strip()
        return ProcessedInput(
            input_type=InputType.COMMAND_PROMPT,
            raw_text=user_input,
            prompt_name=prompt_name,
        )

    # Resource loading
    if user_input.startswith("/resource/"):
        resource_uri = user_input.removeprefix("/resource/").strip()
        return ProcessedInput(
            input_type=InputType.COMMAND_RESOURCE,
            raw_text=user_input,
            resource_uri=resource_uri,
        )

    # Anything else starting with "/" is unknown
    return ProcessedInput(
        input_type=InputType.UNKNOWN_COMMAND,
        raw_text=user_input,
    )
