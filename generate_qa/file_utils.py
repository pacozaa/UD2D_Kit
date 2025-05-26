#!/usr/bin/env python3
"""File utilities for Q&A generation."""

from pathlib import Path
from typing import List

# Define paths
# MARKDOWN_DIR = Path("palo-web-md")
# OUTPUT_DIR = Path("qa_dataset")


def get_markdown_files(source_dir: Path, limit: int = None) -> List[Path]:
    """Get markdown files from the palo-web-md directory.

    Args:
        limit: Maximum number of files to return. If None, return all files.

    Returns:
        List of Path objects for markdown files.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    md_files = [f for f in source_dir.iterdir() if f.is_file()
                and f.suffix == '.md']

    # Sort files by name for consistent order
    md_files.sort()

    if limit and limit > 0:
        return md_files[:limit]
    return md_files
