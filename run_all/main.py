#!/usr/bin/env python3
"""
Main module for run_all functionality that combines crawling and Q&A generation.
"""

from .arguments import parse_arguments
from generate_qa.main import main as generate_qa_main
from crawl.crawler import DFSCrawler
from crawl.main import run_crawler
import asyncio
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional

import sys
import importlib.util

# Import modules using a more reliable approach for package boundaries
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_crawl(args) -> Dict[str, Any]:
    """Run the web crawling process with provided arguments.

    Args:
        args: Command line arguments for crawling

    Returns:
        Dict[str, Any]: Statistics from the crawl operation
    """
    print("=" * 60)
    print(f"Step 1: Web Crawling - {args.url}")
    print("=" * 60)

    print(f"Starting URL: {args.url}")
    print(f"Maximum depth: {args.max_depth}")
    print(f"Maximum pages: {args.max_pages}")
    print(f"Output Markdown directory: {os.path.abspath(args.output_md)}")
    print(f"Output HTML directory: {os.path.abspath(args.output_html)}")
    print("=" * 60)

    # Start crawling process
    start_time = time.time()
    crawl_stats = asyncio.run(run_crawler(args))
    end_time = time.time()

    # Print summary
    print("\nCrawl Summary:")
    print("-" * 60)
    print(f"Total pages crawled: {crawl_stats['urls_crawled']}")
    print(f"Successful crawls: {crawl_stats['successful_crawls']}")
    print(f"Failed crawls: {crawl_stats['failed_crawls']}")
    print(f"Total URLs found: {crawl_stats['total_urls_found']}")
    print(
        f"URLs skipped (already visited): {crawl_stats['urls_skipped_already_visited']}")
    print(f"URLs skipped (max depth): {crawl_stats['urls_skipped_max_depth']}")
    if args.same_domain_only:
        print(
            f"URLs skipped (different domain): {crawl_stats['urls_skipped_different_domain']}")
    print(f"URLs skipped (invalid): {crawl_stats['urls_skipped_invalid']}")
    print(f"Markdown files saved: {crawl_stats['markdown_files_saved']}")
    print(f"HTML files saved: {crawl_stats['html_files_saved']}")
    print(f"Total time: {end_time - start_time:.2f} seconds")

    print("-" * 60)
    print(f"Markdown files saved in: {os.path.abspath(args.output_md)}")
    print(f"HTML files saved in: {os.path.abspath(args.output_html)}")
    print("=" * 60)

    return crawl_stats


def run_qa_generation(args) -> None:
    """Run the Q&A generation process with provided arguments.

    Args:
        args: Command line arguments for Q&A generation
    """
    print("\n\n")
    print("=" * 60)
    print("Step 2: Q&A Generation")
    print("=" * 60)

    source_dir = Path(args.output_md)
    output_dir = Path(args.qa_output)

    print(f"Processing markdown files from: {source_dir}")
    print(f"Saving QA pairs to: {output_dir}")

    if args.qa_all:
        print("Processing all markdown files")
    else:
        print(f"Processing {args.num_files} markdown files")

    print(f"Generating {args.num_qa_pairs} Q&A pairs per file")
    print("=" * 60)

    # We need to run Q&A generation with a separate process to avoid argument conflicts
    import subprocess
    import sys

    qa_command = [
        sys.executable, "-m", "generate_qa",
        f"--input={args.output_md}",
        f"--output={args.qa_output}",
        f"--num-pairs={args.num_qa_pairs}"
    ]

    if args.qa_all:
        qa_command.append("--all")
    else:
        qa_command.append(f"n={args.num_files}")

    result = subprocess.run(qa_command, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"Error during Q&A generation. Return code: {result.returncode}")
    else:
        print("Q&A generation completed successfully!")


def main() -> None:
    """Main function to orchestrate the entire process - crawling and Q&A generation."""
    # Parse command-line arguments
    args = parse_arguments()

    # Print banner
    print("=" * 60)
    print("Web To Dataset: Crawling + Q&A Generation")
    print("=" * 60)

    # Step 1: Run crawler
    crawl_stats = run_crawl(args)

    # Step 2: Run QA generation
    run_qa_generation(args)

    # Final summary
    print("\n\n")
    print("=" * 60)
    print("Process Complete!")
    print(f"Crawled {crawl_stats['successful_crawls']} pages from {args.url}")
    print(f"Generated Q&A pairs saved to: {os.path.abspath(args.qa_output)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
