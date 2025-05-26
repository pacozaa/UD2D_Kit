#!/usr/bin/env python3
"""Pydantic models for web crawling."""

from pydantic import BaseModel, Field


class CrawlStats(BaseModel):
    """Statistics collected during web crawling."""

    total_urls_found: int = Field(
        default=0, description="Total number of URLs discovered during crawling")
    urls_crawled: int = Field(
        default=0, description="Number of URLs actually crawled")
    urls_skipped_already_visited: int = Field(
        default=0, description="URLs skipped because they were already visited")
    urls_skipped_max_depth: int = Field(
        default=0, description="URLs skipped because they exceed max depth")
    urls_skipped_different_domain: int = Field(
        default=0, description="URLs skipped because they are from a different domain")
    urls_skipped_invalid: int = Field(
        default=0, description="URLs skipped because they are invalid")
    successful_crawls: int = Field(
        default=0, description="Number of successful crawls")
    failed_crawls: int = Field(
        default=0, description="Number of failed crawls")
    markdown_files_saved: int = Field(
        default=0, description="Number of markdown files saved")
    html_files_saved: int = Field(
        default=0, description="Number of HTML files saved")
    total_time_seconds: float = Field(
        default=0.0, description="Total time spent crawling in seconds")
