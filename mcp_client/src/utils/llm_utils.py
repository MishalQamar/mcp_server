from dataclasses import dataclass
from typing import Any

from google.genai import Client as GenAIClient
from google.genai import types

from ..settings import settings


@dataclass
class LLMClient:
    """Small wrapper around the Gemini client."""

    model_id: str
    config: types.GenerateContentConfig

    def __post_init__(self) -> None:
        self.client = GenAIClient()

    async def generate_content(self, conversation_history: list[dict[str, Any]]):
        """Generate a response from the model using the current conversation history."""
        contents = []

        for message in conversation_history:
            role = "user" if message["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=message["content"])],
                )
            )

        response = await self.client.aio.models.generate_content(
            model=self.model_id,
            contents=contents,
            config=self.config,
        )
        return response


def build_llm_config_with_tools(
    mcp_tools: list,
    thinking_enabled: bool = True,
) -> types.GenerateContentConfig:
    """Build Gemini config with MCP tools converted into Gemini function declarations."""
    gemini_tools = []

    for tool in mcp_tools:
        gemini_tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name=tool.name,
                    description=tool.description,
                    parameters=tool.inputSchema,
                )
            ]
        )
        gemini_tools.append(gemini_tool)

    thinking_config = types.ThinkingConfig(
        include_thoughts=thinking_enabled,
        thinking_budget=settings.thinking_budget,
    )

    return types.GenerateContentConfig(
        tools=gemini_tools,
        thinking_config=thinking_config,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )


def extract_first_function_call(response) -> tuple[str, dict] | None:
    """Extract the first function call from a model response, if present."""
    if not response.candidates:
        return None

    content = response.candidates[0].content
    if not content or not content.parts:
        return None

    for part in content.parts:
        if getattr(part, "function_call", None):
            function_call = part.function_call
            return function_call.name, dict(function_call.args)

    return None


def extract_final_answer(response) -> str:
    """Extract the final text answer from the model response."""
    if not response.candidates:
        return ""

    content = response.candidates[0].content
    if not content or not content.parts:
        return ""

    text_parts = []
    for part in content.parts:
        if getattr(part, "text", None):
            text_parts.append(part.text)

    return "\n".join(text_parts).strip()


def extract_thought_summary(response) -> str:
    """Extract thought text from the model response, if available."""
    if not response.candidates:
        return ""

    content = response.candidates[0].content
    if not content or not content.parts:
        return ""

    thought_parts = []
    for part in content.parts:
        if getattr(part, "thought", None):
            thought_parts.append(str(part.thought))
        elif getattr(part, "text", None) and "[THOUGHT]" in part.text:
            thought_parts.append(part.text)

    return "\n".join(thought_parts).strip()
