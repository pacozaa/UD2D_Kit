#!/usr/bin/env python3
"""Arguments parsing for Q&A generation."""

import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate Q&A pairs from markdown files")
    parser.add_argument("--all", action="store_true",
                        help="Process all markdown files")
    parser.add_argument("n", nargs="?", default="5",
                        help="Number of files to process (default: 5)")

    args = parser.parse_args()

    # Handle n=X format
    if not args.all and "=" in args.n:
        args.n = args.n.split("=")[1]

    return args
