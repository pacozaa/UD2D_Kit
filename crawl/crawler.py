#!/usr/bin/env python3
"""
Core crawler implementation with depth-first search strategy using crawl4ai.
"""

import asyncio
import time
from typing import List, Dict, Set, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
import json
import os

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, DefaultMarkdownGenerator, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter

from .utils import is_valid_url, is_same_domain, sanitize_filename, save_markdown, save_html
from .models import CrawlStats


class DFSCrawler:
    """A depth-first search web crawler using crawl4ai."""

    def __init__(
        self,
        start_url: str,
        max_depth: int = 3,
        max_pages: int = 30,
        output_md_dir: str = "crawl_output",
        output_html_dir: str = "crawl_html",
        delay: float = 1.0,
        verbose: bool = False,
        timeout: int = 30,
        same_domain_only: bool = True,
    ):
        """Initialize the DFS crawler.

        Args:
            start_url: The starting URL for crawling
            max_depth: Maximum crawling depth
            max_pages: Maximum number of pages to crawl
            output_md_dir: Directory to save Markdown files
            output_html_dir: Directory to save HTML files
            delay: Delay between requests in seconds
            verbose: Whether to enable verbose output
            timeout: Timeout for requests in seconds
            same_domain_only: Whether to crawl only URLs from the same domain
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.output_md_dir = output_md_dir
        self.output_html_dir = output_html_dir
        self.delay = delay
        self.verbose = verbose
        self.timeout = timeout
        self.same_domain_only = same_domain_only

        # Initialize state
        self.visited_urls: Set[str] = set()
        self.crawled_pages = 0
        self.url_stack: List[Tuple[str, int]] = [
            (start_url, 0)]  # (url, depth)

        # Ensure output directories exist
        os.makedirs(output_md_dir, exist_ok=True)
        os.makedirs(output_html_dir, exist_ok=True)

        # Extract domain from start_url for same-domain filtering
        self.start_domain = urlparse(start_url).netloc

    async def crawl(self) -> CrawlStats:
        """Perform depth-first search crawling.

        Returns:
            CrawlStats: Crawling statistics
        """
        start_time = time.time()
        stats = CrawlStats()

        if self.verbose:
            print(f"Starting DFS crawl from {self.start_url}")
            print(f"Maximum depth: {self.max_depth}")
            print(f"Maximum pages: {self.max_pages}")
            print(f"Same domain only: {self.same_domain_only}")

        async with AsyncWebCrawler() as crawler:
            # Configure the markdown generator with content filtering
            markdown_generator = DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()  # Use pruning filter for cleaner markdown
            )

            # Process URLs in DFS order
            while self.url_stack and self.crawled_pages < self.max_pages:
                # Get the next URL from the stack (DFS)
                current_url, current_depth = self.url_stack.pop()

                # Skip if URL already visited
                if current_url in self.visited_urls:
                    stats.urls_skipped_already_visited += 1
                    continue

                # Skip if exceeding max depth
                if current_depth > self.max_depth:
                    stats.urls_skipped_max_depth += 1
                    continue

                if self.verbose:
                    print(
                        f"\nCrawling [{self.crawled_pages + 1}/{self.max_pages}] {current_url} (depth: {current_depth})")

                # Mark as visited before crawling to avoid duplicates
                self.visited_urls.add(current_url)
                self.crawled_pages += 1

                # Create a config for this crawl
                run_config = CrawlerRunConfig(
                    markdown_generator=markdown_generator,
                    cache_mode=CacheMode.BYPASS,  # Always get fresh content
                )

                try:
                    # Execute the crawl for current URL
                    result = await crawler.arun(url=current_url, config=run_config)

                    if result.success:
                        stats.successful_crawls += 1

                        # Generate safe filenames
                        safe_filename = sanitize_filename(current_url)

                        # Save HTML content
                        if hasattr(result, 'html') and result.html:
                            html_path = save_html(
                                result.html, self.output_html_dir, safe_filename)
                            if html_path:
                                stats.html_files_saved += 1

                        # Save Markdown content
                        if result.markdown and result.markdown.fit_markdown:
                            md_path = save_markdown(
                                result.markdown.fit_markdown,
                                self.output_md_dir,
                                safe_filename
                            )
                            if md_path:
                                stats.markdown_files_saved += 1

                        # Process links if not at max depth
                        if current_depth < self.max_depth:
                            # Get links from result
                            links = []
                            if result.links:
                                # Add internal links first (important for DFS priority)
                                if 'internal' in result.links and result.links['internal']:
                                    if self.verbose:
                                        print(
                                            f"  Internal links: {len(result.links['internal'])}")
                                    links.extend(
                                        [link['href'] for link in result.links['internal']])

                                # Add external links if not restricted to same domain
                                if not self.same_domain_only and 'external' in result.links and result.links['external']:
                                    if self.verbose:
                                        print(
                                            f"  External links: {len(result.links['external'])}")
                                    links.extend(
                                        [link['href'] for link in result.links['external']])

                            stats.total_urls_found += len(links)

                            # Process and add links to the stack in reverse order
                            # (so the first link is processed first in DFS)
                            new_links = []
                            for link in links:
                                # Make URL absolute if relative
                                if not link.startswith(('http://', 'https://')):
                                    link = urljoin(current_url, link)

                                # Skip invalid URLs
                                if not is_valid_url(link):
                                    stats.urls_skipped_invalid += 1
                                    continue

                                # Skip URLs not in the same domain if same_domain_only is True
                                if self.same_domain_only and not is_same_domain(link, self.start_url):
                                    stats.urls_skipped_different_domain += 1
                                    continue

                                # Skip already visited URLs
                                if link in self.visited_urls:
                                    stats.urls_skipped_already_visited += 1
                                    continue

                                # Add to new_links for processing
                                new_links.append((link, current_depth + 1))

                            # Add new links to stack in reverse order for proper DFS
                            for link in reversed(new_links):
                                self.url_stack.append(link)
                    else:
                        stats.failed_crawls += 1
                        if self.verbose:
                            print(f"  Failed to crawl: {result.error_message}")

                except Exception as e:
                    stats.failed_crawls += 1
                    if self.verbose:
                        print(f"  Error crawling {current_url}: {str(e)}")

                # Apply delay between requests
                if self.url_stack and self.crawled_pages < self.max_pages:
                    if self.verbose:
                        print(
                            f"  Waiting {self.delay} seconds before next request...")
                    await asyncio.sleep(self.delay)

        # Calculate total time
        total_time = time.time() - start_time
        stats.total_time_seconds = total_time
        stats.urls_crawled = self.crawled_pages

        if self.verbose:
            print("\nCrawl completed!")
            print(f"Total time: {total_time:.2f} seconds")
            print(f"URLs crawled: {self.crawled_pages}")
            print(f"Markdown files saved: {stats.markdown_files_saved}")
            print(f"HTML files saved: {stats.html_files_saved}")

        return stats
