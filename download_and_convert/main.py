#!/usr/bin/env python3
"""
Main execution module for downloading and converting web pages to Markdown.
"""

import os
import time
from typing import List, Tuple, Dict, Any

from .arguments import parse_arguments
from .link_utils import extract_links_from_markdown, sanitize_filename
from .downloader import download_web_page
from .converter import convert_html_to_markdown


def main() -> None:
    """Main function to orchestrate the download and conversion process."""
    # Parse command-line arguments
    args = parse_arguments()

    # Ensure directories exist
    os.makedirs(args.download_dir, exist_ok=True)
    os.makedirs(args.markdown_dir, exist_ok=True)

    if args.verbose:
        print("DEBUG: Module execution started")

    print("Starting download and conversion process...")

    # Extract links from the markdown file
    print(f"Looking for file: {os.path.abspath(args.input_file)}")
    links = extract_links_from_markdown(args.input_file)
    print(f"Found {len(links)} links in {args.input_file}")

    successful_downloads = 0
    successful_conversions = 0

    # Process each link
    for index, (text, url) in enumerate(links, 1):
        print(f"\nProcessing link {index}/{len(links)}: {text} - {url}")

        # Create a filename for the downloaded HTML
        html_filename = sanitize_filename(url)
        html_path = os.path.join(args.download_dir, html_filename)

        # Generate a corresponding markdown filename
        md_filename = os.path.splitext(html_filename)[0] + '.md'
        md_path = os.path.join(args.markdown_dir, md_filename)

        # Download the web page
        download_success = download_web_page(
            url,
            html_path,
            max_retries=args.max_retries,
            verbose=args.verbose
        )

        if download_success:
            successful_downloads += 1

            # Convert to Markdown
            conversion_success = convert_html_to_markdown(
                html_path,
                md_path,
                verbose=args.verbose
            )

            if conversion_success:
                successful_conversions += 1

        # Add a delay between requests to be respectful to the servers
        if args.verbose and index < len(links):
            print(f"Waiting {args.delay} seconds before the next request...")

        time.sleep(args.delay)

    print("\nSummary:")
    print(f"Total links processed: {len(links)}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Successfully converted to Markdown: {successful_conversions}")
    print(f"Downloaded files saved in: {os.path.abspath(args.download_dir)}")
    print(f"Markdown files saved in: {os.path.abspath(args.markdown_dir)}")
