from pathlib import Path


def build_result_message(
    research_directory: str,
    processed: int,
    local_files: list[str],
    dest_folder: Path,
    warnings: list[str],
    errors: list[str],
) -> str:
    """Build a readable summary message for local file processing."""
    message = (
        f"Processed {processed}/{len(local_files)} local files from "
        f"'{research_directory}'. Output directory: {dest_folder.resolve()}."
    )

    if warnings:
        message += f" Warnings: {len(warnings)}."
    if errors:
        message += f" Errors: {len(errors)}."

    return message
