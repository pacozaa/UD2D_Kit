#!/usr/bin/env python3
"""PDF utilities for Q&A generation."""

from pathlib import Path
from typing import List, Tuple, Dict

from PyPDF2 import PdfReader


def get_pdf_files(source_dir: Path, limit: int = None) -> List[Path]:
    """Get PDF files from the source directory.

    Args:
        source_dir: Directory containing PDF files.
        limit: Maximum number of files to return. If None, return all files.

    Returns:
        List of Path objects for PDF files.
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    pdf_files = [f for f in source_dir.iterdir() if f.is_file()
                 and f.suffix.lower() == '.pdf']

    # Sort files by name for consistent order
    pdf_files.sort()

    if limit and limit > 0:
        return pdf_files[:limit]
    return pdf_files


def extract_pdf_content(pdf_file: Path) -> Dict[int, str]:
    """Extract text content from a PDF file, organized by page numbers.

    Args:
        pdf_file: Path to the PDF file.

    Returns:
        Dictionary mapping page numbers (0-indexed) to page content.
    """
    try:
        reader = PdfReader(pdf_file)
        page_contents = {}

        for i, page in enumerate(reader.pages):
            content = page.extract_text()
            if content.strip():  # Only include non-empty pages
                page_contents[i] = content

        return page_contents
    except Exception as e:
        print(f"Error extracting content from {pdf_file}: {e}")
        return {}
