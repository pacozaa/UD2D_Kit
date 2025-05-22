#!/usr/bin/env python3
"""
Module for downloading web pages from URLs.
"""

import time
from typing import Union, Optional, List, Dict, Any
import requests


def download_web_page(
    url: str,
    output_path: str,
    max_retries: int = 3,
    verbose: bool = False
) -> bool:
    """Download a web page and save it to the specified path.

    Args:
        url: The URL of the web page to download
        output_path: The path where the HTML file should be saved
        max_retries: Maximum number of retry attempts for failed downloads
        verbose: Whether to print verbose output

    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # Send request with a timeout and retry mechanism
        for attempt in range(max_retries):
            try:
                if verbose:
                    print(
                        f"Attempt {attempt + 1}/{max_retries} downloading: {url}")

                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an exception for 4XX/5XX responses
                break
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    print(
                        f"Retry {attempt + 1}/{max_retries} for {url}: {str(e)}")
                    time.sleep(2)  # Wait before retrying
                else:
                    raise

        # Write the HTML content to a file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

        print(f"Successfully downloaded: {url} -> {output_path}")
        return True

    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False
