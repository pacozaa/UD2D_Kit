# Q&A Dataset Generator

A Python tool for generating question-answer pairs from markdown files using OpenAI's API.

## Overview

This tool iterates through markdown files in the `palo-web-md` folder, uses OpenAI's GPT models to generate question-answer pairs based on the content, and saves the results to a JSONL file. It's particularly useful for creating training datasets for question-answering systems or for content comprehension testing.

## Requirements

- Python 3.6+
- OpenAI API key
- Required Python packages:
  - openai
  - tqdm

## Installation

1. Ensure you have Python installed on your system.
2. Install the required packages:

```bash
pip install openai tqdm
```

3. Set your OpenAI API key as an environment variable (recommended):

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Alternatively, the script will prompt you to enter your API key if it's not found in the environment.

## Usage

The script offers several ways to run it based on how many files you want to process:

### Process Default Number of Files (5)

```bash
python generate_qa.py
```

This will process the first 5 markdown files in the `palo-web-md` directory.

### Process a Specific Number of Files

```bash
python generate_qa.py n=10
```

This will process the first 10 markdown files in the `palo-web-md` directory.

### Process All Files

```bash
python generate_qa.py --all
```

This will process all markdown files in the `palo-web-md` directory.

## Output

The script generates a JSONL file in the `qa_dataset` directory with a timestamp in the filename (e.g., `qa_pairs_20250520_144539.jsonl`).

Each line in the JSONL file represents a single question-answer pair in JSON format:

```json
{
  "question": "What is PALO IT's main industry?",
  "answer": "PALO IT operates in IT Services and IT Consulting.",
  "source": "company_palo-it.md"
}
```

Each entry includes:

- The question
- The answer
- The source markdown file

## Customization

You can modify the script to adjust:

- The number of Q&A pairs generated per file (default: 20)
- The OpenAI model used (default: "gpt-4o-2024-08-06")
- The input/output directories
- The prompt used to generate the Q&A pairs

To change the number of pairs or modify the system prompt, edit the `generate_qa_pairs` function in the script.

## Example Workflow

1. Prepare markdown files in the `palo-web-md` directory.
2. Run the script with your preferred options:
   ```bash
   python generate_qa.py --all
   ```
3. Check the `qa_dataset` directory for the output JSONL file.
4. Use the generated Q&A pairs for your applications or further processing.

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set as an environment variable or enter it when prompted.
- **Rate Limiting**: The script includes a delay between API calls to avoid rate limiting. If you still encounter rate limits, consider increasing the delay in the script.
- **File Handling Errors**: Make sure the `palo-web-md` directory exists and contains markdown files.

## Limitations

- The quality of the generated Q&A pairs depends on the content of the markdown files and the capabilities of the OpenAI model used.
- Processing a large number of files may take significant time and incur API costs.
- The script does not currently support nested directories of markdown files.

## License

This tool is provided for educational and demonstration purposes. Please ensure you comply with OpenAI's usage policies when using this script.
