"""
tool_functions.py

This module provides utility functions for horoscope generation and file reading.

Functions:
----------
get_horoscope(sign):
    Returns a humorous horoscope message for the given zodiac sign.

get_file(path_dict):
    Reads and returns the contents of a file specified by the 'filename' key in the path_dict dictionary.
    If the file is not found, prints an error message and returns None.
"""
from typing import Dict

def get_horoscope(sign: str) -> str:
    """Returns your horoscpose"""
    return f"{sign}: Next Tuesday you will befriend a baby otter."

def get_file(path_dict: Dict[str, str]) -> str:
    """
    Gets the contents of a file
    Expects
    
    """
    try:
        with open(path_dict['filename'], 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {path_dict['filename']}")
        return None

