#!/usr/bin/env python3
"""
Module for handling command line arguments for the web crawler functionality.
"""

import argparse
from typing import Tuple


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for web crawling.

    Returns:
        Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Web crawler with depth-first search strategy using crawl4ai library.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "url",
        type=str,
        help="Starting URL for web crawling"
    )

    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum depth for crawling"
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=30,
        help="Maximum number of pages to crawl"
    )

    parser.add_argument(
        "--output-md",
        type=str,
        default="crawl_output",
        help="Directory to save converted Markdown files"
    )

    parser.add_argument(
        "--output-html",
        type=str,
        default="crawl_html",
        help="Directory to save downloaded HTML files"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between requests"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds for each request"
    )

    parser.add_argument(
        "--same-domain-only",
        action="store_true",
        default=True,
        help="Crawl only pages from the same domain as the starting URL"
    )

    return parser.parse_args()
