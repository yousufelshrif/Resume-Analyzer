"""
InterestExtractor Module

This module provides the InterestExtractor class for parsing and extracting personal interests 
or hobbies from unstructured resume text. It searches for section headers such as "Interests", 
"Hobbies", or "Activities", and returns a clean list of individual interest items.

The extractor removes bullet points, dashes, and other common delimiters, and splits multi-item lines
into separate entries. It is useful for resume parsing pipelines, candidate profiling, or personalizing 
job recommendations.

Classes:
    InterestExtractor: Extracts a list of interests or hobbies from resume content.
    
Dependencies:
    - re: for efficient regex matching
    - collections: for efficient data structures and operations
    - typing: for type hints and annotations
    
Typical Use Cases:
    - Resume parsing and candidate enrichment
    - Automated career profiling
    - HR chatbots and career advisory tools
    - Matching candidates to job culture or team fit
"""



import re
from typing import List, Optional


class InterestExtractor:
    """
    A utility class to extract interests or hobbies from resume text.

    This class identifies common sections labeled as 'Interests', 'Hobbies', or 
    'Activities' and returns a list of individual interest items by cleaning and 
    splitting section content.

    Methods:
        extract(text: str) -> Optional[List[str]]:
            Extracts a list of interests from the resume text.
    """

    def __init__(self):
        """
        Initializes the InterestExtractor with standard section header keywords.
        """
        self.interest_headers = ["interests", "hobbies", "personal interests", "activities"]

    def extract(self, text: str) -> Optional[List[str]]:
        """
        Extract interests or hobbies from resume text.

        Args:
            text (str): Full resume content as a string.

        Returns:
            Optional[List[str]]: A list of extracted interest strings, or None if not found.
        """
        if not text or not isinstance(text, str):
            return None

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        interests_section = []
        start_collecting = False

        for line in lines:
            lower_line = line.lower().strip()

            if any(header in lower_line for header in self.interest_headers):
                start_collecting = True
                continue

            # Stop collecting if another major section starts (e.g., "Education:", "Skills:")
            if start_collecting and (re.match(r'^[A-Z][a-zA-Z ]+:$', line) or len(line.split()) <= 2):
                break

            if start_collecting:
                interests_section.append(line)

        # Clean and split interest lines
        cleaned = []
        for line in interests_section:
            line = re.sub(r'^[-•\s]+', '', line)
            parts = re.split(r'[•\-–•]', line)
            for part in parts:
                part = part.strip()
                if part:
                    cleaned.append(part)

        return cleaned if cleaned else None
