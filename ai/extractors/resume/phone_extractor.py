"""
This module provides the PhoneExtractor class for extracting and optionally formatting phone numbers 
from unstructured text, such as resumes, documents, or scraped content. It handles common obfuscations 
(e.g., digit words like "zero", "one", or "[at]", "[dot]") and supports both local and international 
number formats.

Features:
    - Extract phone numbers with 10 or more digits
    - Normalize obfuscated formats (e.g., "zero one two" → "012")
    - Optional formatting of local numbers (e.g., "(123) 456-7890")
    - Supports returning a single match or all matches found

Classes:
    PhoneExtractor: A class for extracting and formatting phone numbers from plain text.
    
Dependencies:
    - re: for efficient regex matching
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume and CV parsers
    - Contact information extraction
    - Web scraping and text mining
    - Customer onboarding tools
"""

import re
from typing import List, Optional, Union


class PhoneExtractor:
    """
    A utility class to extract and optionally format phone numbers from unstructured text.
    Supports common digit obfuscations and formatting styles. It can detect international and
    local phone numbers with optional normalization.

    Methods:
        extract(text: str, return_all: bool = False, format_output: bool = False) -> Union[str, List[str], None]:
            Extracts and optionally formats phone numbers from text.
    """

    def __init__(self):
        """
        Initialize the PhoneExtractor with digit word replacements and obfuscation mappings.
        """
        self.replacements = {
            "[dot]": ".", "[at]": "@", " at ": "@", "(at)": "@",
            "zero": "0", "one": "1", "two": "2", "three": "3",
            "four": "4", "five": "5", "six": "6", "seven": "7",
            "eight": "8", "nine": "9"
        }

    def extract(
        self,
        text: str,
        return_all: bool = False,
        format_output: bool = False
    ) -> Union[str, List[str], None]:
        """
        Extract and optionally format phone numbers from raw text using regex.

        Args:
            text (str): Raw text (e.g., resume content or scraped HTML).
            return_all (bool): If True, return all matched phone numbers. Otherwise, return the first.
            format_output (bool): If True, format local 10-digit numbers as (XXX) XXX-XXXX.

        Returns:
            Union[str, List[str], None]: The extracted phone number(s), or None if no match is found.
        """
        if not text or not isinstance(text, str):
            return None

        cleaned = text.lower()
        for word, digit in self.replacements.items():
            cleaned = cleaned.replace(word, digit)

        # Detect sequences that resemble phone numbers
        potential_numbers = re.findall(r'\+?\d[\d\s().-]{8,}\d', cleaned)

        results = set()
        for raw in potential_numbers:
            cleaned_number = re.sub(r'(?!^\+)[^\d]', '', raw)  # keep "+" at the start
            if len(cleaned_number) >= 10:
                if format_output and cleaned_number.startswith('+'):
                    formatted = cleaned_number  # leave international format untouched
                elif format_output:
                    formatted = f"({cleaned_number[:3]}) {cleaned_number[3:6]}-{cleaned_number[6:10]}"
                else:
                    formatted = cleaned_number
                results.add(formatted)

        sorted_phones = sorted(results)

        if not sorted_phones:
            return None

        return sorted_phones if return_all else sorted_phones[0]
