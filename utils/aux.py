"""
aux.py

This module provides utility functions for processing code blocks.

Functions:
----------
extract_code_blocks(text: str) -> List[str]:
    Extracts all code blocks from a markdown-formatted string.
    Returns a list containing the contents of each code block, excluding the triple backtick markers.
"""

from typing import List
import re

def extract_code_blocks(text: str) -> List[str]:
    """
    Extract all code blocks from markdown text.
    Returns a list of code content (without the ``` markers).
    """
    # Pattern to match code blocks with optional language specification
    pattern = r'```(?:\w+)?\n?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]