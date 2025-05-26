#!/usr/bin/env python3
"""Main module for Q&A generation."""

import json
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from tqdm import tqdm

from .models import QAPair
from .arguments import parse_arguments, FileType
from .file_utils import get_file_getter_function
from .markdown_processor import process_markdown_file
from .pdf_processor import process_pdf_file


def main(source_dir: Optional[Path] = None, output_dir: Optional[Path] = None,
         num_files: Optional[int] = None, all_files: bool = False, num_pairs: Optional[int] = None,
         file_type: Optional[str] = None):
    """Main function to process files and generate QA pairs.

    Args:
        source_dir: Optional custom input directory. If provided, overrides the command-line argument.
        output_dir: Optional custom output directory. If provided, overrides the command-line argument.
        num_files: Optional number of files to process. If provided, overrides the command-line argument.
        all_files: Whether to process all files. If provided, overrides the command-line argument.
        num_pairs: Optional number of QA pairs to generate per file/page. If provided, overrides the command-line argument.
        file_type: Optional file type to process. If provided, overrides the command-line argument.
    """
    args = parse_arguments()

    # Override args with provided parameters if they exist
    use_all = all_files if all_files is not None else args.all
    num_qa_pairs = num_pairs if num_pairs is not None else args.num_pairs
    file_type_value = file_type if file_type is not None else args.file_type

    # Use provided output_dir or the one from command line args
    output_dir = output_dir or Path(args.output)

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Use provided source_dir or the one from command line args
    source_dir = Path(source_dir) if source_dir else Path(args.input)

    # Print the directories being used
    print(f"Input directory: {source_dir}")
    print(f"Output directory: {output_dir}")
    print(f"File type: {file_type_value}")

    # Get the appropriate file getter function based on file type
    get_files = get_file_getter_function(file_type_value)

    # Get files
    if use_all:
        files = get_files(source_dir=source_dir)
        print(f"Processing all {len(files)} {file_type_value} files")
    else:
        try:
            n_files = num_files if num_files is not None else int(args.n)
            files = get_files(source_dir=source_dir, limit=n_files)
            print(f"Processing {n_files} {file_type_value} files")
        except ValueError:
            print(f"Invalid number of files: {args.n}. Using default (5).")
            files = get_files(source_dir=source_dir, limit=5)

    if not files:
        print(f"No {file_type_value} files found in {source_dir}")
        return

    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"qa_pairs_{timestamp}.jsonl"

    # Print the output file path
    print(f"Output file: {output_file}")

    # Process files based on file type
    all_qa_pairs: List[QAPair] = []
    file_processor = process_pdf_file if file_type_value == FileType.PDF else process_markdown_file

    for file_path in tqdm(files, desc="Processing files"):
        file_qa_pairs = file_processor(file_path, num_qa_pairs)
        all_qa_pairs.extend(file_qa_pairs)

        # Small delay between files to avoid rate limiting
        time.sleep(1)

    # Write all QA pairs to a single JSONL file
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa_pair in all_qa_pairs:
            f.write(json.dumps(qa_pair.model_dump(), ensure_ascii=False) + '\n')

    print(f"\nGenerated {len(all_qa_pairs)} QA pairs from {len(files)} files")
    print(f"Results saved to {output_file}")
