#!/usr/bin/env python3
"""
Utility functions for working with links from Markdown files and creating filenames.
"""

import re
from typing import List, Tuple
from urllib.parse import urlparse


def extract_links_from_markdown(file_path: str) -> List[Tuple[str, str]]:
    """Extract all links from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        List of tuples containing link text and URL
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract links using regex
    # This pattern matches markdown link format: [link text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, content)

    links = []
    for text, url in matches:
        # Skip anchor links (links that start with #)
        if url.startswith('#'):
            continue

        # Only include web URLs
        if url.startswith('http'):
            links.append((text, url))

    return links


def sanitize_filename(url: str) -> str:
    """Create a safe filename from a URL.

    Args:
        url: The URL to sanitize

    Returns:
        A sanitized filename with .html extension
    """
    # Parse the URL to get the path
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Remove leading and trailing slashes
    path = path.strip('/')

    # Replace slashes and other problematic characters with underscores
    filename = re.sub(r'[\\/:*?"<>|]', '_', path)

    # Ensure filename is not too long and has a .html extension
    if len(filename) > 200:
        filename = filename[:200]

    if not filename:
        # If we have no path (e.g., just a domain), use the hostname
        filename = parsed_url.netloc.replace('.', '_')

    return f"{filename}.html"
