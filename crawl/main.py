#!/usr/bin/env python3
"""
Main execution module for web crawling with depth-first search strategy.
"""

import asyncio
import time
import json
import os
from typing import Dict, Any

from .arguments import parse_arguments
from .crawler import DFSCrawler


async def run_crawler(args) -> Dict[str, Any]:
    """Run the DFS crawler with provided arguments.

    Args:
        args: Command line arguments

    Returns:
        Dict[str, Any]: Statistics from the crawl operation
    """
    # Initialize and run the crawler
    crawler = DFSCrawler(
        start_url=args.url,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        output_md_dir=args.output_md,
        output_html_dir=args.output_html,
        delay=args.delay,
        verbose=args.verbose,
        timeout=args.timeout,
        same_domain_only=args.same_domain_only,
    )

    # Start crawling
    stats = await crawler.crawl()
    return stats


def main() -> None:
    """Main function to orchestrate the web crawling process."""
    # Parse command-line arguments
    args = parse_arguments()

    # Print banner
    print("=" * 60)
    print(f"DFS Web Crawler - crawl4ai")
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

    # Save stats to a JSON file
    stats_file = os.path.join(args.output_md, "crawl_stats.json")
    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(crawl_stats, f, indent=2)
        print(f"Saved crawl statistics to {stats_file}")
    except Exception as e:
        print(f"Failed to save statistics: {e}")

    print("-" * 60)
    print(f"Markdown files saved in: {os.path.abspath(args.output_md)}")
    print(f"HTML files saved in: {os.path.abspath(args.output_html)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
