#!/usr/bin/env python3
"""Markdown processing utilities for Q&A generation."""

from pathlib import Path
from typing import List

from tqdm import tqdm

from .models import QAPair
from .openai_utils import generate_qa_pairs


def process_markdown_file(file_path: Path, num_qa_pairs: int) -> List[QAPair]:
    """Process a markdown file and generate QA pairs.

    Args:
        file_path: Path to the markdown file
        num_qa_pairs: Number of QA pairs to generate

    Returns:
        List of generated QA pairs
    """
    try:
        # Read markdown content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate QA pairs
        print(f"\nProcessing {file_path.name}...")
        qa_pairs = generate_qa_pairs(content, num_pairs=num_qa_pairs)

        if qa_pairs:
            # Add file source information to each QA pair
            for qa_pair in qa_pairs:
                qa_pair.source = file_path.name

            print(f"Generated {len(qa_pairs)} QA pairs from {file_path.name}")
        else:
            print(f"No QA pairs generated for {file_path.name}")

        return qa_pairs

    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return []
