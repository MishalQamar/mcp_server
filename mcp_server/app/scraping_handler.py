import asyncio
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx


async def scrape_url(url: str) -> dict:
    """
    Fetch a single URL and return a structured scraping result.

    Returns a dictionary with:
    - url
    - title
    - markdown
    - success
    """
    timeout = httpx.Timeout(30.0)

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        html = response.text
        title_match = re.search(
            r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL
        )
        title = title_match.group(1).strip() if title_match else "Untitled"

        # Very simple HTML-to-text cleanup for the rebuild stage
        text = re.sub(r"(?is)<script.*?>.*?</script>", "", html)
        text = re.sub(r"(?is)<style.*?>.*?</style>", "", text)
        text = re.sub(r"(?is)<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return {
            "url": url,
            "title": title,
            "markdown": text,
            "success": True,
        }

    except Exception as e:
        return {
            "url": url,
            "title": "Scraping Failed",
            "markdown": f"Error scraping {url}: {str(e)}",
            "success": False,
        }


async def clean_markdown(
    markdown_content: str, article_guidelines: str = "", url_for_log: str = ""
) -> str:
    """
    Clean scraped markdown/text content.

    This rebuild version keeps cleaning simple:
    - collapse extra blank lines
    - trim whitespace
    """
    if not markdown_content.strip():
        return markdown_content

    cleaned = re.sub(r"\n{3,}", "\n\n", markdown_content)
    return cleaned.strip()


async def scrape_urls_concurrently(
    urls: list[str],
    concurrency_limit: int = 4,
    article_guidelines: str = "",
) -> list[dict]:
    """
    Scrape multiple URLs concurrently with a semaphore limit.
    """
    semaphore = asyncio.Semaphore(concurrency_limit)

    async def scrape_and_clean(url: str) -> dict:
        async with semaphore:
            result = await scrape_url(url)
            if result.get("success", False):
                result["markdown"] = await clean_markdown(
                    result["markdown"],
                    article_guidelines=article_guidelines,
                    url_for_log=url,
                )
            return result

    tasks = [scrape_and_clean(url) for url in urls]
    return await asyncio.gather(*tasks)


def slugify_url_to_filename(url: str) -> str:
    """
    Convert a URL into a safe markdown filename.
    """
    parsed = urlparse(url)
    base = f"{parsed.netloc}{parsed.path}".strip("/")

    if not base:
        base = "index"

    base = base.replace("/", "-")
    base = re.sub(r"[^a-zA-Z0-9._-]+", "-", base)
    base = re.sub(r"-{2,}", "-", base).strip("-")

    if not base.endswith(".md"):
        base += ".md"

    return base.lower()


def write_scraped_results_to_files(
    completed_results: list[dict],
    output_dir: Path,
) -> tuple[list[str], int]:
    """
    Write successful scraped results to markdown files.

    Returns:
        (saved_filenames, successful_scrapes_count)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files: list[str] = []
    successful_scrapes = 0

    for result in completed_results:
        if not result.get("success", False):
            continue

        filename = slugify_url_to_filename(result["url"])
        output_path = output_dir / filename

        content = (
            f"# {result['title']}\n\n"
            f"Source URL: {result['url']}\n\n"
            f"{result['markdown']}\n"
        )

        output_path.write_text(content, encoding="utf-8")
        saved_files.append(filename)
        successful_scrapes += 1

    return saved_files, successful_scrapes
