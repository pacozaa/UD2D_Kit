#!/usr/bin/env python3
"""
Module for converting HTML files to Markdown format.
"""

from markitdown import MarkItDown


def convert_html_to_markdown(html_path: str, md_path: str, verbose: bool = False) -> bool:
    """Convert an HTML file to Markdown using MarkItDown.

    Args:
        html_path: Path to the HTML file to convert
        md_path: Path where the Markdown file should be saved
        verbose: Whether to print verbose output

    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Initialize MarkItDown without any special parameters
        md = MarkItDown()

        if verbose:
            print(f"Converting {html_path} to Markdown...")

        # Convert the HTML content to Markdown
        result = md.convert(html_path)

        # Write the Markdown content to a file
        with open(md_path, 'w', encoding='utf-8') as md_file:
            md_file.write(result.text_content)

        print(f"Successfully converted: {html_path} -> {md_path}")
        return True

    except Exception as e:
        print(f"Failed to convert {html_path}: {str(e)}")
        return False
