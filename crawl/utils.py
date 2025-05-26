#!/usr/bin/env python3
"""
Utility functions for web crawler.
"""

import os
import re
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Set, Any, Optional
import base64


def is_valid_url(url: str) -> bool:
    """Check if URL is valid.

    Args:
        url: URL to check

    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs belong to the same domain.

    Args:
        url1: First URL
        url2: Second URL

    Returns:
        bool: True if both URLs have the same domain, False otherwise
    """
    try:
        domain1 = urlparse(url1).netloc
        domain2 = urlparse(url2).netloc
        return domain1 == domain2
    except Exception:
        return False


def sanitize_filename(url: str) -> str:
    """Create a safe filename from URL.

    Args:
        url: URL to convert to a filename

    Returns:
        str: Sanitized filename
    """
    parsed_url = urlparse(url)
    # Use both netloc and path to create unique filenames
    path = parsed_url.path

    # Replace path separators with underscores
    path = path.replace('/', '_')

    # Remove query parameters
    path = path.rstrip('_')

    # Combine domain and path
    filename = f"{parsed_url.netloc}{path}"

    # Replace any remaining invalid characters with underscores
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)

    # If filename is empty (e.g. from root URL), use 'index'
    if not filename or filename == parsed_url.netloc:
        filename = f"{parsed_url.netloc}_index"

    return filename


def save_screenshot(screenshot_data: str, output_dir: str, filename: str) -> str:
    """Save a base64 screenshot to a file.

    Args:
        screenshot_data: Base64-encoded screenshot data
        output_dir: Directory to save the screenshot
        filename: Base filename without extension

    Returns:
        str: Path to saved screenshot
    """
    os.makedirs(output_dir, exist_ok=True)
    screenshot_path = os.path.join(output_dir, f"{filename}.png")

    try:
        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(screenshot_data))
        return screenshot_path
    except Exception as e:
        print(f"Error saving screenshot: {e}")
        return ""


def save_html(html_content: str, output_dir: str, filename: str) -> str:
    """Save HTML content to a file.

    Args:
        html_content: HTML content to save
        output_dir: Directory to save the HTML
        filename: Base filename without extension

    Returns:
        str: Path to saved HTML file
    """
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, f"{filename}.html")

    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return html_path
    except Exception as e:
        print(f"Error saving HTML: {e}")
        return ""


def save_markdown(markdown_content: str, output_dir: str, filename: str) -> str:
    """Save Markdown content to a file.

    Args:
        markdown_content: Markdown content to save
        output_dir: Directory to save the Markdown
        filename: Base filename without extension

    Returns:
        str: Path to saved Markdown file
    """
    os.makedirs(output_dir, exist_ok=True)
    md_path = os.path.join(output_dir, f"{filename}.md")

    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        return md_path
    except Exception as e:
        print(f"Error saving Markdown: {e}")
        return ""
