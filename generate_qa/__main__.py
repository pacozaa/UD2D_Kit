#!/usr/bin/env python3
"""
Entry point for running the generate_qa module directly.

Usage:
    python -m generate_qa            # Process 5 files by default
    python -m generate_qa n=10       # Process 10 files
    python -m generate_qa --all      # Process all files
"""

from .main import main

if __name__ == "__main__":
    main()
