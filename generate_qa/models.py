#!/usr/bin/env python3
"""Pydantic models for Q&A generation."""

from typing import List, Optional
from pydantic import BaseModel, Field


class QAPair(BaseModel):
    """A single question-answer pair."""
    question: str = Field(
        description="The question generated from the content")
    answer: str = Field(description="The answer to the question")
    source: Optional[str] = Field(None, description="Source file")
    page: Optional[int] = Field(
        None, description="Page number for PDF files (0-indexed)")


class QAPairResponse(BaseModel):
    """Response structure containing multiple QA pairs."""
    qa_pairs: List[QAPair] = Field(description="List of question-answer pairs")
