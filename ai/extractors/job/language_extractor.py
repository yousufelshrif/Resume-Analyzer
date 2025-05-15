"""
JobLanguageExtractor Module

This module provides the JobLanguageExtractor class for identifying spoken or written
language requirements mentioned in job descriptions. It supports detection of over
30 global languages and can be customized with additional entries.

The extractor performs exact case-insensitive matching using regular expressions
and returns a deduplicated list of mentioned languages.

Classes:
    JobLanguageExtractor: Extracts required or preferred languages from job text.

Typical Use Cases:
    - Job parsing for multilingual roles
    - Resume-language matching
    - HR systems and ATS integrations

"""


import re
from typing import List, Optional


class JobLanguageExtractor:
    """
    A class to extract language requirements from job description text.

    Detects mentions of spoken or written language proficiency such as
    "Fluent in English", "Arabic is a plus", or "Must speak French".

    Attributes:
        language_list (List[str]): List of supported language names to match.
    """

    def __init__(self, known_languages: Optional[List[str]] = None):
        """
        Initializes the extractor with a default or custom list of languages.

        Args:
            known_languages (Optional[List[str]]): Custom list of language names.
        """
        self.language_list = known_languages or [
            "English", "Arabic", "French", "German", "Spanish", "Italian", "Mandarin",
            "Chinese", "Hindi", "Japanese", "Korean", "Portuguese", "Russian", "Turkish",
            "Dutch", "Bengali", "Urdu", "Polish", "Tamil", "Telugu", "Swedish", "Hebrew",
            "Malay", "Thai", "Vietnamese", "Greek", "Czech", "Romanian", "Hungarian",
            "Finnish", "Ukrainian", "Persian", "Punjabi", "Serbian", "Croatian"
        ]

    def extract(self, text: str) -> List[str]:
        """
        Extracts required languages from the job description.

        Args:
            text (str): Raw job description text.

        Returns:
            List[str]: Sorted, deduplicated list of mentioned languages.
        """
        lower_text = text.lower()
        results = set()

        for lang in self.language_list:
            pattern = rf"\b{re.escape(lang.lower())}\b"
            if re.search(pattern, lower_text):
                results.add(lang)

        return sorted(results)
    
    
if __name__ == "__main__":
    jd_text = """
    Requirements:
    - Fluent in English, Arabic is a plus
    - Candidates must be able to communicate in French or Spanish
    - Working knowledge of Japanese preferred
    """

    extractor = JobLanguageExtractor()
    print(extractor.extract(jd_text))
    
    

