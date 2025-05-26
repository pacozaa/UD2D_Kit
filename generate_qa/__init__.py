#!/usr/bin/env python3
"""
Generate Q&A pairs from markdown or PDF files using OpenAI's API.

This module provides functionality to generate question-answer pairs from markdown or PDF files,
using OpenAI's API, and save the results to a JSONL file.
"""

from .models import QAPair, QAPairResponse
from .arguments import parse_arguments, FileType
from .file_utils import get_markdown_files, get_file_getter_function
from .openai_utils import generate_qa_pairs
from .pdf_utils import get_pdf_files, extract_pdf_content
from .markdown_processor import process_markdown_file
from .pdf_processor import process_pdf_file
from .main import main

__all__ = [
    "QAPair",
    "QAPairResponse",
    "parse_arguments",
    "FileType",
    "get_markdown_files",
    "process_markdown_file",
    "process_pdf_file",
    "get_pdf_files",
    "extract_pdf_content",
    "get_file_getter_function",
    "generate_qa_pairs",
    "main",
]
