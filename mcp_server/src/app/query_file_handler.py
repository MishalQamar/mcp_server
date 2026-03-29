from pathlib import Path


def write_queries_to_file(
    output_path: Path, queries_and_reasons: list[tuple[str, str]]
) -> None:
    """
    Write generated queries and reasons to a markdown file.
    """
    lines: list[str] = ["# Next Research Queries", ""]

    for i, (question, reason) in enumerate(queries_and_reasons, start=1):
        lines.append(f"## Query {i}")
        lines.append(f"Question: {question}")
        lines.append(f"Reason: {reason}")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
