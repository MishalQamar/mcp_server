import json
import shutil
from pathlib import Path
from typing import Any

from ..app.local_files_handler import build_result_message
from ..app.notebook_handler import NotebookToMarkdownConverter
from ..config.constants import (
    GUIDELINES_FILENAMES_FILE,
    LOCAL_FILES_FROM_RESEARCH_FOLDER,
    NOVA_FOLDER,
)
from ..utils.file_utils import read_file_safe


def process_local_files_tool(research_directory: str) -> dict[str, Any]:
    """
    Process local files referenced in the extracted guidelines metadata.

    Reads .nova/guidelines_filenames.json, processes each local file in
    "local_file_paths", and writes the results into
    .nova/local_files_from_research.

    - .py and .md files are copied
    - .ipynb files are converted to markdown
    """
    research_path = Path(research_directory)
    nova_path = research_path / NOVA_FOLDER
    metadata_path = nova_path / GUIDELINES_FILENAMES_FILE

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Guidelines metadata file not found: {metadata_path.resolve()}"
        )

    data = json.loads(read_file_safe(metadata_path))
    local_files = data.get("local_file_paths", [])

    if not local_files:
        dest_folder = nova_path / LOCAL_FILES_FROM_RESEARCH_FOLDER
        dest_folder.mkdir(parents=True, exist_ok=True)

        return {
            "status": "success",
            "files_processed": 0,
            "files_total": 0,
            "processed_files": [],
            "warnings": [],
            "errors": [],
            "output_directory": str(dest_folder.resolve()),
            "message": "No local files found to process.",
        }

    dest_folder = nova_path / LOCAL_FILES_FROM_RESEARCH_FOLDER
    dest_folder.mkdir(parents=True, exist_ok=True)

    processed = 0
    processed_files: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []

    notebook_converter = NotebookToMarkdownConverter(
        include_outputs=True,
        include_metadata=False,
    )

    for rel_path in local_files:
        src_path = research_path / rel_path
        dest_name = rel_path.replace("/", "_").replace("\\", "_")

        try:
            if not src_path.exists():
                warnings.append(f"File not found: {rel_path}")
                continue

            if src_path.suffix.lower() == ".ipynb":
                dest_name = dest_name.rsplit(".ipynb", 1)[0] + ".md"
                dest_path = dest_folder / dest_name

                markdown_content = notebook_converter.convert_notebook_to_string(
                    src_path
                )
                dest_path.write_text(markdown_content, encoding="utf-8")

            else:
                dest_path = dest_folder / dest_name
                shutil.copy2(src_path, dest_path)

            processed += 1
            processed_files.append(dest_name)

        except Exception as e:
            errors.append(f"Failed to process {rel_path}: {str(e)}")

    result_message = build_result_message(
        research_directory=research_directory,
        processed=processed,
        local_files=local_files,
        dest_folder=dest_folder,
        warnings=warnings,
        errors=errors,
    )

    return {
        "status": "success" if processed > 0 else "warning",
        "files_processed": processed,
        "files_total": len(local_files),
        "processed_files": processed_files,
        "warnings": warnings,
        "errors": errors,
        "output_directory": str(dest_folder.resolve()),
        "message": result_message,
    }
