from pathlib import Path

import nbformat


class NotebookToMarkdownConverter:
    """
    Convert Jupyter notebooks into a readable markdown string for LLM consumption.
    """

    def __init__(self, include_outputs: bool = True, include_metadata: bool = False):
        self.include_outputs = include_outputs
        self.include_metadata = include_metadata

    def convert_notebook_to_string(self, notebook_path: str | Path) -> str:
        """
        Read a .ipynb file and convert it into a single markdown string.
        """
        notebook_path = Path(notebook_path)

        nb = nbformat.read(notebook_path, as_version=4)

        parts: list[str] = []

        if self.include_metadata and nb.metadata:
            parts.append("# Notebook Metadata")
            parts.append("```json")
            parts.append(str(nb.metadata))
            parts.append("```")
            parts.append("")

        for i, cell in enumerate(nb.cells, start=1):
            if cell.cell_type == "markdown":
                parts.append(f"## Markdown Cell {i}")
                parts.append(cell.source)
                parts.append("")

            elif cell.cell_type == "code":
                parts.append(f"## Code Cell {i}")
                parts.append("```python")
                parts.append(cell.source)
                parts.append("```")
                parts.append("")

                if self.include_outputs and getattr(cell, "outputs", None):
                    output_text = self._format_outputs(cell.outputs)
                    if output_text:
                        parts.append(f"### Output of Code Cell {i}")
                        parts.append(output_text)
                        parts.append("")

            else:
                parts.append(f"## {cell.cell_type.capitalize()} Cell {i}")
                parts.append(cell.source)
                parts.append("")

        return "\n".join(parts).strip()

    def _format_outputs(self, outputs: list) -> str:
        """
        Convert notebook outputs into readable markdown text.
        """
        rendered_outputs: list[str] = []

        for output in outputs:
            output_type = output.get("output_type", "")

            if output_type == "stream":
                text = output.get("text", "")
                if text:
                    rendered_outputs.append("```text")
                    rendered_outputs.append(text.rstrip())
                    rendered_outputs.append("```")

            elif output_type in {"execute_result", "display_data"}:
                data = output.get("data", {})

                if "text/plain" in data:
                    rendered_outputs.append("```text")
                    rendered_outputs.append(str(data["text/plain"]).rstrip())
                    rendered_outputs.append("```")

            elif output_type == "error":
                traceback = output.get("traceback", [])
                if traceback:
                    rendered_outputs.append("```text")
                    rendered_outputs.extend(traceback)
                    rendered_outputs.append("```")

        return "\n".join(rendered_outputs).strip()
