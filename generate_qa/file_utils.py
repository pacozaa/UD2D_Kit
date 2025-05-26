#!/usr/bin/env python3
"""File utilities for Q&A generation."""

from pathlib import Path
from typing import List, Callable

from .arguments import FileType


def get_markdown_files(source_dir: Path, limit: int = None) -> List[Path]:
    """Get markdown files from the source directory.

    Args:
        source_dir: Directory containing markdown files.
        limit: Maximum number of files to return. If None, return all files.

    Returns:
        List of Path objects for markdown files.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    md_files = [f for f in source_dir.iterdir() if f.is_file()
                and f.suffix.lower() == '.md']

    # Sort files by name for consistent order
    md_files.sort()

    if limit and limit > 0:
        return md_files[:limit]
    return md_files


def get_file_getter_function(file_type: str) -> Callable[[Path, int], List[Path]]:
    """Get the appropriate file getter function based on file type.

    Args:
        file_type: Type of files to get (markdown, pdf)

    Returns:
        Function to get files of the specified type
    """
    if file_type == FileType.PDF:
        from .pdf_utils import get_pdf_files
        return get_pdf_files

    # Default to markdown
    return get_markdown_files
