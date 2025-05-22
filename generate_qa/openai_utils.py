#!/usr/bin/env python3
"""OpenAI utilities for Q&A generation."""

import os
import getpass
from typing import List

import openai
from dotenv import load_dotenv

from .models import QAPair, QAPairResponse


# Load environment variables from .env file
load_dotenv()

# Configure OpenAI client - check for API key
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    api_key = getpass.getpass(
        "OpenAI API Key not found in environment. Please enter your API key: ")
    if not api_key:
        raise ValueError("API key is required to use OpenAI API")

client = openai.OpenAI(api_key=api_key)


def generate_qa_pairs(md_content: str, num_pairs: int = 20) -> List[QAPair]:
    """Generate question-answer pairs using OpenAI API.

    Args:
        md_content: Markdown content to generate QA pairs from
        num_pairs: Number of QA pairs to generate

    Returns:
        List of QAPair objects containing questions and answers
    """
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            response_format=QAPairResponse,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that generates {num_pairs} question-answer pairs based on the provided markdown content. The questions should cover different aspects of the content and be diverse."},
                {"role": "user", "content": md_content}
            ]
        )

        # Access the parsed data directly (no need for json.loads)
        return completion.choices[0].message.parsed.qa_pairs

    except Exception as e:
        print(f"Error generating QA pairs: {e}")
        return []
