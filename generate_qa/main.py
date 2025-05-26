#!/usr/bin/env python3
"""Main module for Q&A generation."""

import json
import time
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from tqdm import tqdm

from .models import QAPair
from .arguments import parse_arguments
from .file_utils import get_markdown_files
from .openai_utils import generate_qa_pairs


def main(source_dir: Optional[Path] = None, output_dir: Optional[Path] = None,
         num_files: Optional[int] = None, all_files: bool = False, num_pairs: Optional[int] = None):
    """Main function to process markdown files and generate QA pairs.

    Args:
        source_dir: Optional custom input directory. If provided, overrides the command-line argument.
        output_dir: Optional custom output directory. If provided, overrides the command-line argument.
        num_files: Optional number of files to process. If provided, overrides the command-line argument.
        all_files: Whether to process all files. If provided, overrides the command-line argument.
        num_pairs: Optional number of QA pairs to generate per file. If provided, overrides the command-line argument.
    """
    args = parse_arguments()

    # Override args with provided parameters if they exist
    use_all = all_files if all_files is not None else args.all
    num_qa_pairs = num_pairs if num_pairs is not None else args.num_pairs

    # Use provided output_dir or the one from command line args
    output_dir = output_dir or Path(args.output)

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Use provided source_dir or the one from command line args
    source_dir = Path(source_dir) if source_dir else Path(args.input)

    # Print the directories being used
    print(f"Input directory: {source_dir}")
    print(f"Output directory: {output_dir}")

    # Get markdown files
    if use_all:
        md_files = get_markdown_files(source_dir=source_dir)
        print(f"Processing all {len(md_files)} markdown files")
    else:
        try:
            n_files = num_files if num_files is not None else int(args.n)
            md_files = get_markdown_files(
                source_dir=source_dir, limit=n_files)
            print(f"Processing {n_files} markdown files")
        except ValueError:
            print(f"Invalid number of files: {args.n}. Using default (5).")
            md_files = get_markdown_files(source_dir=source_dir, limit=5)

    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"qa_pairs_{timestamp}.jsonl"

    # Print the output file path
    print(f"Output file: {output_file}")
    # Process markdown files
    all_qa_pairs: List[QAPair] = []

    for md_file in tqdm(md_files, desc="Processing files"):
        try:
            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Generate QA pairs
            print(f"\nProcessing {md_file.name}...")
            qa_pairs = generate_qa_pairs(md_content, num_pairs=num_qa_pairs)

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
