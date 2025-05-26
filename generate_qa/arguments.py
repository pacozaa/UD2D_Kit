#!/usr/bin/env python3
"""Arguments parsing for Q&A generation."""

import argparse
from enum import Enum, auto


class FileType(str, Enum):
    """Enum for file types."""
    MARKDOWN = "markdown"
    PDF = "pdf"


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate Q&A pairs from markdown or PDF files")
    parser.add_argument("--all", action="store_true",
                        help="Process all files")
    parser.add_argument("--input", type=str, default="crawl_output",
                        help="Directory containing input files (default: crawl_output)")
    parser.add_argument("--output", type=str, default="qa_dataset",
                        help="Directory to save generated Q&A pairs (default: qa_dataset)")
    parser.add_argument("--num-pairs", type=int, default=5,
                        help="Number of Q&A pairs to generate per file/page (default: 5)")
    parser.add_argument("--file-type", type=str, choices=[ft.value for ft in FileType],
                        default=FileType.MARKDOWN.value,
                        help="Type of files to process (default: markdown)")
    parser.add_argument("n", nargs="?", default="5",
                        help="Number of files to process (default: 5)")

    args = parser.parse_args()

    # Handle n=X format
    if not args.all and "=" in args.n:
        args.n = args.n.split("=")[1]

    return args
