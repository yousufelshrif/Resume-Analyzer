"""
LanguageExtractor Module

This module provides the LanguageExtractor class, which identifies spoken or written languages 
from unstructured text such as resumes, CVs, or job descriptions. The class supports a default 
set of major world languages, and also allows the use of a custom list.

It performs exact word boundary matching (e.g., matches "French" but not "Frenchman"), 
making it suitable for precise language extraction in NLP pipelines or HR automation tools.

Classes:
    LanguageExtractor: Extracts language mentions from raw text.

Dependencies:
    - re: for efficient regex matching
    - collections: for efficient data structures and operations
"""


import re
from typing import List, Optional


class LanguageExtractor:
    """
    A utility class to extract spoken or written languages from resume or job description text.

    Attributes:
        language_list (List[str]): A predefined or user-supplied list of language names to detect.

    Methods:
        extract(text: str) -> Optional[List[str]]:
            Extracts language names found in the given text.
    """

    def __init__(self, known_languages: Optional[List[str]] = None):
        """
        Initializes the LanguageExtractor with a list of known languages.

        Args:
            known_languages (List[str], optional): Custom list of languages to detect.
                If None, a default list of major world languages is used.
        """
        self.language_list = known_languages or [
            "English", "Arabic", "French", "German", "Spanish", "Italian", "Mandarin",
            "Chinese", "Hindi", "Japanese", "Korean", "Portuguese", "Russian", "Turkish",
            "Dutch", "Bengali", "Urdu", "Polish", "Tamil", "Telugu", "Swedish", "Hebrew",
            "Malay", "Thai", "Vietnamese", "Greek", "Czech", "Romanian", "Hungarian",
            "Finnish", "Ukrainian", "Persian", "Punjabi", "Serbian", "Croatian"
        ]

    def extract(self, text: str) -> Optional[List[str]]:
        """
        Extracts spoken or written languages from resume text.

        Args:
            text (str): Raw resume or job description text.

        Returns:
            Optional[List[str]]: Sorted list of detected language names, or None if none found.
        """
        if not text or not isinstance(text, str):
            return None

        lower_text = text.lower()
        results = set()

        for lang in self.language_list:
            pattern = rf"\b{re.escape(lang.lower())}\b"
            if re.search(pattern, lower_text):
                results.add(lang)

        return sorted(results) if results else None
