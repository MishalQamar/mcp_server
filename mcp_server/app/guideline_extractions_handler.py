import re


def extract_urls(text: str) -> list[str]:
    """Extract all HTTP/HTTPS URLs from the given text."""
    url_pattern = re.compile(r"https?://[^\s)>\"',]+")
    return url_pattern.findall(text)


def extract_local_paths(text: str) -> list[str]:
    """
    Extract local file references ending in .py, .ipynb, or .md.

    This is a simplified version for the first rebuild.
    """
    path_pattern = re.compile(r"(?<!https?://)([\w./\\-]+\.(?:py|ipynb|md))")
    return list(dict.fromkeys(path_pattern.findall(text)))
