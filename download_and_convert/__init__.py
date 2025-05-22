"""
Download and Convert Module

This module provides functionalities to download web content from URLs
and convert HTML files to Markdown format.
"""

from .arguments import parse_arguments
from .link_utils import extract_links_from_markdown, sanitize_filename
from .downloader import download_web_page
from .converter import convert_html_to_markdown
from .main import main

__all__ = [
    'parse_arguments',
    'extract_links_from_markdown',
    'sanitize_filename',
    'download_web_page',
    'convert_html_to_markdown',
    'main',
]
