#!/usr/bin/env python3
"""
Module for handling command line arguments for the run_all functionality.
"""

import argparse
from typing import Tuple


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for run_all module that combines crawling and Q&A generation.

    Returns:
        Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Combine web crawling and Q&A generation into a single command.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Crawling arguments
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

    # Q&A generation arguments
    parser.add_argument(
        "--qa-all",
        action="store_true",
        help="Process all markdown files for QA generation"
    )

    parser.add_argument(
        "--qa-output",
        type=str,
        default="qa_dataset",
        help="Directory to save generated Q&A pairs"
    )

    parser.add_argument(
        "--num-qa-pairs",
        type=int,
        default=5,
        help="Number of Q&A pairs to generate per file"
    )

    parser.add_argument(
        "--num-files",
        type=int,
        default=5,
        help="Number of files to process for QA generation"
    )

    return parser.parse_args()
