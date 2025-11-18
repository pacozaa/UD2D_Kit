# Unstructured Data To Dataset Kit(UD2D_Kit)

> 🚀 **Transform web content and PDFs into high-quality Q&A datasets for LLM training and RAG evaluation in minutes, not days!**

## Quick Start

Get up and running in 3 simple steps:

```bash
# 1. Create and activate environment
conda create -n unstructured-data-to-dataset python=3.10
conda activate unstructured-data-to-dataset

# 2. Install the package
pip install -e .

# 3. Set up your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 4. Run end-to-end: crawl a website and generate Q&A pairs
python -m run_all "https://example.com" --max-depth=2 --max-pages=10 --num-qa-pairs=5
```

That's it! Your Q&A dataset will be saved in the `qa_dataset` directory as a JSONL file.

## Overview

Unstructured Data To Dataset is a comprehensive Python toolkit designed for enterprise LLM specialists and RAG (Retrieval-Augmented Generation) developers to efficiently build training and evaluation datasets from web content and PDF documents. This project streamlines the process of converting organizational websites and documents into structured question-answer datasets suitable for fine-tuning language models or evaluating RAG systems.

The toolkit provides a modular workflow that:

1. **Crawls websites** with configurable depth and scope parameters
2. **Converts HTML to Markdown** for easier content processing
3. **Processes PDF documents** to extract and structure content
4. **Generates high-quality Q&A pairs** leveraging OpenAI's API
5. **Outputs structured data** in JSONL format ready for model training or evaluation

With minimal setup and configuration, developers can transform domain-specific web content and PDF documents into valuable datasets for enhancing LLM capabilities with organizational knowledge.

## Installation

1. Set up Conda environment:

```bash
conda create -n unstructured-data-to-dataset python=3.10
conda activate unstructured-data-to-dataset
```

2. Install the required packages:

```bash
pip install -e .
```

## Usage

### Crawl a Website

The crawl module uses a depth-first search (DFS) strategy to crawl websites using the `crawl4ai` library. It downloads HTML pages and converts them to Markdown files.

#### Basic Usage

```bash
python -m crawl "https://example.com" --max-depth=3 --max-pages=30
```

#### Command Line Arguments

| Argument           | Description                                               | Default      |
| ------------------ | --------------------------------------------------------- | ------------ |
| url                | Starting URL for web crawling (required)                  | -            |
| --max-depth        | Maximum depth for crawling                                | 3            |
| --max-pages        | Maximum number of pages to crawl                          | 30           |
| --output-md        | Directory to save converted Markdown files                | crawl_output |
| --output-html      | Directory to save downloaded HTML files                   | crawl_html   |
| --delay            | Delay in seconds between requests                         | 1.0          |
| --verbose          | Enable verbose output                                     | False        |
| --timeout          | Timeout in seconds for each request                       | 30           |
| --same-domain-only | Crawl only pages from the same domain as the starting URL | True         |

#### Examples

E-commerce test site:

```bash
python -m crawl "https://webscraper.io/test-sites/e-commerce/allinone" --max-depth=3 --max-pages=10 --verbose
```

API testing site with reduced depth:

```bash
python -m crawl "https://httpbin.org" --max-depth=2 --max-pages=5 --verbose
```

Wikipedia with custom output directories:

```bash
python -m crawl "https://www.wikipedia.org" --max-depth=2 --max-pages=5 --output-md="wiki_md" --output-html="wiki_html"
```

MDN Web Docs (Mozilla Developer Network):

```bash
crawl "https://developer.mozilla.org/en-US/docs/Web/JavaScript" --max-depth=2 --max-pages=5 --output-md="mdn_md" --output-html="mdn_html" --verbose
```

### Generate Q&A Pairs from Markdown or PDF Files

The generate_qa module uses OpenAI's API to create question-answer pairs from markdown or PDF files. It processes files (by default from the `crawl_output` directory) and generates a JSONL file containing Q&A pairs.

#### Basic Usage

```bash
python -m generate_qa
```

This will process the default number of files (5) from the input directory.

#### Command Line Arguments

| Argument    | Description                                 | Default      |
| ----------- | ------------------------------------------- | ------------ |
| n=N         | Number of files to process                  | 5            |
| --all       | Process all files instead of limited number | False        |
| --input     | Directory containing input files            | crawl_output |
| --file-type | Type of files to process (markdown or pdf)  | markdown     |
| --output    | Directory to save generated Q&A pairs       | qa_dataset   |
| --num-pairs | Number of Q&A pairs to generate per file    | 5            |

#### Output

The script generates a timestamped JSONL file in the `qa_dataset` directory (e.g., `qa_pairs_20250526_142015.jsonl`). Each line contains a JSON object with:

- question: The generated question
- answer: The corresponding answer
- source: The source file name
- page: The page number (for PDF files only, 0-indexed)

#### Examples

Process the default number of files (5):

```bash
python -m generate_qa
```

Process a specific number of files:

```bash
python -m generate_qa n=10
```

Process all files in the markdown directory:

```bash
python -m generate_qa --all
```

Process files from a custom input directory and save to a custom output directory:

```bash
python -m generate_qa --input="mdn_md" --output="mdn_qa_dataset"
```

Generate more Q&A pairs per file:

```bash
python -m generate_qa --num-pairs=30
```

```bash
python -m generate_qa --file-type=pdf --num-pairs=1
```

Process PDF files:

```bash
python -m generate_qa --file-type=pdf --input="pdf_documents"
```

Combine multiple options:

```bash
python -m generate_qa n=10 --input="wiki_md" --output="wiki_qa" --num-pairs=25 --file-type=markdown
```

### Run All Steps

The `run_all` module combines the crawling and Q&A generation steps into a single command. It first crawls the specified website and then generates Q&A pairs from the downloaded markdown files.

#### Basic Usage

```bash
python -m run_all "https://example.com" --max-depth=3 --max-pages=30 --num-qa-pairs=5
```

#### Command Line Arguments

| Argument           | Description                                               | Default      |
| ------------------ | --------------------------------------------------------- | ------------ |
| url                | Starting URL for web crawling (required)                  | -            |
| --max-depth        | Maximum depth for crawling                                | 3            |
| --max-pages        | Maximum number of pages to crawl                          | 30           |
| --output-md        | Directory to save converted Markdown files                | crawl_output |
| --output-html      | Directory to save downloaded HTML files                   | crawl_html   |
| --delay            | Delay in seconds between requests                         | 1.0          |
| --verbose          | Enable verbose output                                     | False        |
| --timeout          | Timeout in seconds for each request                       | 30           |
| --same-domain-only | Crawl only pages from the same domain as the starting URL | True         |
| --qa-all           | Process all markdown files for QA generation              | False        |
| --qa-output        | Directory to save generated Q&A pairs                     | qa_dataset   |
| --num-qa-pairs     | Number of Q&A pairs to generate per file                  | 5            |
| --num-files        | Number of files to process for QA generation              | 5            |

#### Examples

E-commerce test site with custom QA settings:

```bash
python -m run_all "https://webscraper.io/test-sites/e-commerce/allinone" --max-depth=2 --max-pages=10 --num-qa-pairs=10 --num-files=5
```

Process all generated markdown files for QA generation:

```bash
python -m run_all "https://httpbin.org" --max-depth=2 --max-pages=5 --qa-all
```

Wikipedia with custom output directories:

```bash
python -m run_all "https://www.wikipedia.org" --max-depth=1 --max-pages=5 --output-md="wiki_md" --output-html="wiki_html" --qa-output="wiki_qa"
```

Process PDF files from a directory:

```bash
python -m generate_qa --file-type=pdf --input="pdf_documents" --num-pairs=10
```
