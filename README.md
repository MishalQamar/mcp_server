# MCP Server

Python **[FastMCP](https://github.com/jlowin/fastmcp)** MCP server for research ingestion: **tools**, one **resource**, and one **prompt**. Give each tool a `research_directory` that contains `article_guideline.md` (artifacts go under `.nova/`). Connect from Cursor or any MCP host over **stdio**.

## Tools

- **`extract_guidelines_urls`** — Parse the guideline file; classify GitHub, YouTube, and other URLs plus local paths; save metadata for later steps.
- **`process_local_files`** — Process local paths from that metadata.
- **`scrape_and_clean_other_urls`** — Scrape and clean non-GitHub, non-YouTube URLs (optional `concurrency_limit`).
- **`process_github_urls`** — Turn GitHub URLs into markdown digests.
- **`transcribe_youtube_urls`** — Turn YouTube URLs into markdown transcripts.

## Resource

- **`system://memory`** — Current process memory stats (RSS, VMS, percent).

## Prompt

- **`full_research_instructions`** — Workflow instructions for the research agent.

## Requirements

- Python **3.13+** and **[uv](https://docs.astral.sh/uv/)**
- **`mcp_server/.env`** for API keys and model settings as needed (see **`mcp_server/pyproject.toml`** for dependencies)

## Run

```bash
cd mcp_server
uv sync
uv run mcp-server
```

Point your MCP host at this command with **stdio**; run it with working directory **`mcp_server`** so `uv run` resolves correctly.
