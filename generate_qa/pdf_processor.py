#!/usr/bin/env python3
"""PDF processing utilities for Q&A generation."""

from pathlib import Path
from typing import List
import time

from tqdm import tqdm

from .models import QAPair
from .pdf_utils import extract_pdf_content
from .openai_utils import generate_qa_pairs


def process_pdf_file(file_path: Path, num_qa_pairs: int) -> List[QAPair]:
    """Process a PDF file and generate QA pairs for each page.

    Args:
        file_path: Path to the PDF file
        num_qa_pairs: Number of QA pairs to generate per page

    Returns:
        List of generated QA pairs
    """
    try:
        # Extract PDF content by pages
        page_contents = extract_pdf_content(file_path)

        if not page_contents:
            print(f"No text content extracted from {file_path.name}")
            return []

        print(
            f"\nProcessing PDF {file_path.name} with {len(page_contents)} pages...")
        all_qa_pairs: List[QAPair] = []

        for page_num, content in tqdm(page_contents.items(), desc=f"Processing pages in {file_path.name}"):
            # Generate QA pairs for this page
            qa_pairs = generate_qa_pairs(content, num_pairs=num_qa_pairs)

            if qa_pairs:
                # Add file source and page information to each QA pair
                for qa_pair in qa_pairs:
                    qa_pair.source = file_path.name
                    qa_pair.page = page_num

                all_qa_pairs.extend(qa_pairs)
                print(
                    f"Generated {len(qa_pairs)} QA pairs from {file_path.name} page {page_num+1}")
            else:
                print(
                    f"No QA pairs generated for {file_path.name} page {page_num+1}")

            # Small delay to avoid rate limiting
            time.sleep(1)

        return all_qa_pairs

    except Exception as e:
        print(f"Error processing PDF {file_path.name}: {e}")
        return []
