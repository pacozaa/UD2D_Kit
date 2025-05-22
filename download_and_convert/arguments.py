#!/usr/bin/env python3
"""
Module for handling command line arguments for the download and convert functionality.
"""

import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Download content from links in a Markdown file and convert them to Markdown format.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--input-file",
        type=str,
        default="PALO_LINKS_to_Scrape.md",
        help="Path to the Markdown file containing links to download"
    )

    parser.add_argument(
        "--download-dir",
        type=str,
        default="palo-web",
        help="Directory to save downloaded HTML files"
    )

    parser.add_argument(
        "--markdown-dir",
        type=str,
        default="palo-web-md",
        help="Directory to save converted Markdown files"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between requests"
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum number of retry attempts for failed downloads"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()
