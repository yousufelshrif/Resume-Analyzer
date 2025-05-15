"""
EmailExtractor Module

This module provides the EmailExtractor class for extracting email addresses from unstructured text, 
such as resumes or job postings. It handles common obfuscations like '[at]', '(dot)', and textual 
variations to normalize and identify valid email formats.

Classes:
    EmailExtractor: A class to extract and normalize email addresses from text input.
    
Dependencies:
    - re: for efficient regex matching
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume parsing systems
    - Email extraction for HR automation
    - Web scraping and lead generation
    - Normalizing obfuscated contact details
"""


import re
from typing import List, Optional, Union

class EmailExtractor:
    """
    A utility class to extract email addresses from unstructured text such as resumes,
    including common obfuscated formats (e.g., '[at]', '(dot)', etc.).

    Methods:
        extract(text: str, return_all: bool = False) -> Union[str, List[str], None]:
            Extracts one or more email addresses from the provided text.
    """

    def __init__(self):
        # Define known obfuscations (case-insensitive)
        self.obfuscations = [
            (r'\s?\[at\]\s?', '@'),
            (r'\s?\(at\)\s?', '@'),
            (r'\s+at\s+', '@'),
            (r'\s?\[dot\]\s?', '.'),
            (r'\s?\(dot\)\s?', '.'),
            (r'\s+dot\s+', '.'),
        ]
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

    def extract(self, text: str, return_all: bool = False) -> Union[str, List[str], None]:
        """
        Extract email addresses from a block of text, correcting common obfuscations.

        Args:
            text (str): The input text (e.g., resume content or job post).
            return_all (bool): If True, return all detected emails. If False, return only the first match.

        Returns:
            Union[str, List[str], None]: The first email address (default), a list of all emails,
                                            or None if no match is found.
        """
        if not text or not isinstance(text, str):
            return None

        cleaned_text = text.lower()
        for pattern, replacement in self.obfuscations:
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)

        matches = self.email_pattern.findall(cleaned_text)
        matches = [match.strip(".,;:") for match in matches]
        matches = sorted(set(matches))

        if not matches:
            return None

        return matches if return_all else matches[0]
