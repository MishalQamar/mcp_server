from enum import Enum

from rich import print


class Color(str, Enum):
    """Simple color names used for terminal output."""

    BRIGHT_WHITE = "bright_white"
    CYAN = "cyan"
    GREEN = "green"
    MAGENTA = "magenta"
    YELLOW = "yellow"


def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n[bold cyan]{title}[/bold cyan]")


def print_item(
    name: str,
    description: str | None = None,
    index: int | None = None,
    name_color: Color = Color.BRIGHT_WHITE,
    index_color: Color = Color.YELLOW,
) -> None:
    """Print a named item with an optional index and description."""
    prefix = f"[{index_color}]{index}.[/{index_color}] " if index is not None else ""
    print(f"{prefix}[{name_color}]{name}[/{name_color}]")
    if description:
        print(f"   {description}")


def print_startup_info(tools, resources, prompts) -> None:
    """Print startup information after MCP capability discovery."""
    print("[bold green]Nova MCP Client[/bold green]")
    print(f"[bright_white]- {len(tools)} tools available.[/bright_white]")
    print(f"[bright_white]- {len(resources)} resources available.[/bright_white]")
    print(f"[bright_white]- {len(prompts)} prompts available.[/bright_white]")
    print("[bright_white]- Type '/quit' to exit.[/bright_white]")
    print(
        "[bright_white]- Type '/tools', '/resources', or '/prompts' to list available capabilities.[/bright_white]"
    )
    print(
        "[bright_white]- Type '/prompt/<prompt_name>' to load a prompt.[/bright_white]"
    )
    print(
        "[bright_white]- Type '/resource/<resource_uri>' to view a resource.[/bright_white]"
    )
