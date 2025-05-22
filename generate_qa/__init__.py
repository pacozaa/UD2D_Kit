#!/usr/bin/env python3
"""
Generate Q&A pairs from markdown files using OpenAI's API.

This module provides functionality to generate question-answer pairs from markdown files,
using OpenAI's API, and save the results to a JSONL file.
"""

from .models import QAPair, QAPairResponse
from .arguments import parse_arguments
from .file_utils import get_markdown_files
from .openai_utils import generate_qa_pairs
from .main import main

__all__ = [
    "QAPair",
    "QAPairResponse",
    "parse_arguments",
    "get_markdown_files",
    "generate_qa_pairs",
    "main",
]
