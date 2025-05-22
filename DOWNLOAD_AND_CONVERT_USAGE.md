# Download and Convert Usage Guide

This document provides instructions on how to use the `download_and_convert` module, which downloads web pages from specified links and converts them to Markdown format.

## Overview

The `download_and_convert` module performs two main functions:

1. Downloads HTML content from URLs specified in a Markdown file
2. Converts the downloaded HTML to Markdown format using the MarkItDown library

## Prerequisites

Before using the module, ensure you have the following dependencies installed:

```bash
pip install requests bs4 markitdown
```

Or install all dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Command-Line Arguments

The module accepts the following command-line arguments:

| Argument         | Description                                            | Default                   |
| ---------------- | ------------------------------------------------------ | ------------------------- |
| `--input-file`   | Path to the Markdown file containing links to download | `PALO_LINKS_to_Scrape.md` |
| `--download-dir` | Directory to save downloaded HTML files                | `palo-web`                |
| `--markdown-dir` | Directory to save converted Markdown files             | `palo-web-md`             |
| `--delay`        | Delay in seconds between requests                      | `1.0`                     |
| `--max-retries`  | Maximum number of retry attempts for failed downloads  | `3`                       |
| `--verbose`      | Enable verbose output                                  | `False`                   |

## Input File Format

The input file should be a Markdown file containing links in the standard Markdown format:

```markdown
[Link Text](https://example.com/page)
```

The module will extract all links that begin with `http` and ignore anchor links (those starting with `#`).

## Usage Examples

### Basic Usage

To run the module with default settings:

```bash
python -m download_and_convert
```

Or if you've installed the package:

```bash
download_and_convert
```

### Custom Input File

To specify a different input file:

```bash
python -m download_and_convert --input-file my_links.md
```

### Custom Directories

To specify custom directories for downloads and converted files:

```bash
python -m download_and_convert --download-dir html_files --markdown-dir md_files
```

### Adjust Request Behavior

To customize the delay between requests and retry attempts:

```bash
python -m download_and_convert --delay 2.5 --max-retries 5
```

### Verbose Output

To enable detailed logging:

```bash
python -m download_and_convert --verbose
```

### Combining Options

You can combine multiple options:

```bash
python -m download_and_convert --input-file custom_links.md --download-dir html_files --markdown-dir md_files --delay 2.0 --verbose
```

## What the Module Does

1. Extracts links from the specified Markdown file
2. For each link:
   - Downloads the web page
   - Saves it as HTML in the download directory
   - Converts the HTML to Markdown
   - Saves the Markdown in the markdown directory
3. Outputs a summary of the process, including:
   - Total number of links processed
   - Number of successful downloads
   - Number of successful conversions
   - Paths to the download and markdown directories

## Output

The module creates two directories (if they don't already exist):

- The download directory (default: `palo-web/`) - Contains the downloaded HTML files
- The markdown directory (default: `palo-web-md/`) - Contains the converted Markdown files

File naming is based on the URL path, with special characters replaced by underscores.

## Error Handling

The module includes error handling for:

- Failed downloads (with retry mechanism)
- Failed conversions
- Network timeouts

Errors are reported in the console output but don't stop the overall process.

## Notes

- The module adds a delay between requests to be respectful to web servers (configurable with `--delay`)
- User-Agent headers are set to mimic a standard browser
- The module has a retry mechanism for failed downloads (configurable with `--max-retries`)

## Help Command

For a quick reference on all available options:

```bash
python -m download_and_convert --help
```

This will display the help message with all available options and their descriptions.
Starting download and conversion process...
Found 20 links in PALO_LINKS_to_Scrape.md

Processing link 1/20: About Us - https://www.palo-it.com/en/about-us
Successfully downloaded: https://www.palo-it.com/en/about-us -> palo-web/en_about-us.html
Successfully converted: palo-web/en_about-us.html -> palo-web-md/en_about-us.md

...

Summary:
Total links processed: 20
Successfully downloaded: 18
Successfully converted: 18
Downloaded files saved in: /Users/sarinsuriyakoon/mcp-course/palo-web
Markdown files saved in: /Users/sarinsuriyakoon/mcp-course/palo-web-md

```

```
