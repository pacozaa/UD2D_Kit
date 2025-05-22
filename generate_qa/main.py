#!/usr/bin/env python3
"""Main module for Q&A generation."""

import json
import time
from datetime import datetime
from typing import List

from tqdm import tqdm

from .models import QAPair
from .arguments import parse_arguments
from .file_utils import get_markdown_files, OUTPUT_DIR
from .openai_utils import generate_qa_pairs


def main():
    """Main function to process markdown files and generate QA pairs."""
    args = parse_arguments()

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Get markdown files
    if args.all:
        md_files = get_markdown_files()
        print(f"Processing all {len(md_files)} markdown files")
    else:
        try:
            num_files = int(args.n)
            md_files = get_markdown_files(num_files)
            print(f"Processing {len(md_files)} markdown files")
        except ValueError:
            print(f"Invalid number of files: {args.n}. Using default (5).")
            md_files = get_markdown_files(5)

    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"qa_pairs_{timestamp}.jsonl"

    # Process markdown files
    all_qa_pairs: List[QAPair] = []

    for md_file in tqdm(md_files, desc="Processing files"):
        try:
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Generate QA pairs
            print(f"\nProcessing {md_file.name}...")
            qa_pairs = generate_qa_pairs(md_content)

            if qa_pairs:
                # Add file source information to each QA pair
                for qa_pair in qa_pairs:
                    qa_pair.source = md_file.name

                all_qa_pairs.extend(qa_pairs)
                print(
                    f"Generated {len(qa_pairs)} QA pairs from {md_file.name}")
            else:
                print(f"No QA pairs generated for {md_file.name}")

            # Small delay to avoid rate limiting
            time.sleep(1)

        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

    # Write all QA pairs to a single JSONL file
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa_pair in all_qa_pairs:
            f.write(json.dumps(qa_pair.model_dump(), ensure_ascii=False) + '\n')

    print(
        f"\nGenerated {len(all_qa_pairs)} QA pairs from {len(md_files)} files")
    print(f"Results saved to {output_file}")
