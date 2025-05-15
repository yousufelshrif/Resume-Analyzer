"""
JobExperienceExtractor Module

This module defines the JobExperienceExtractor class, which extracts experience-related
requirements from unstructured job description text.

The extractor identifies:
- Explicit experience mentions (e.g., "3+ years", "at least 5 years")
- Contextual phrases (e.g., "proven experience", "hands-on experience", "track record")
- Job experience constraints such as minimum requirements or preferred backgrounds

It returns a deduplicated list of matched phrases that reflect the job's experience expectations.

Classes:
    JobExperienceExtractor: Extracts experience-related requirements and constraints.

Typical Use Cases:
    - Parsing job descriptions for HR automation
    - Resume-job alignment based on experience
    - Building experience filters for candidate search

Author:
    Your Name

Created:
    May 2025
"""


import re
from typing import List


class JobExperienceExtractor:
    """
    A class to extract experience-related requirements from job description text.

    Detects years of experience, job role mentions, and contextual phrases like
    "X+ years", "minimum of X years", or "proven experience in...".

    Attributes:
        year_pattern (re.Pattern): Regex to detect phrases like "3+ years", "at least 5 years", etc.
        context_keywords (List[str]): Keywords indicating relevant experience-related content.
    """

    def __init__(self):
        """
        Initializes regex patterns for years of experience and context detection.
        """
        self.year_pattern = re.compile(
            r"(\b\d{1,2}\s?\+?\s?(?:\+|plus|or more)?\s?(?:years|yrs)\s?(?:of)?\s?(?:experience|exp)?\b)",
            re.IGNORECASE
        )
        self.context_keywords = [
            "experience in", "hands-on experience", "proven experience", "background in",
            "track record", "prior experience", "extensive experience", "familiarity with",
            "working knowledge", "at least", "minimum of"
        ]

    def extract(self, text: str) -> List[str]:
        """
        Extracts experience requirements from job description text.

        Args:
            text (str): Raw job description content.

        Returns:
            List[str]: A list of relevant experience requirement phrases found in the text.
        """
        lines = [line.strip("•–—-* ") for line in text.split('\n') if line.strip()]
        results = set()

        for line in lines:
            normalized = line.strip()

            # Match patterns like "3+ years of experience"
            year_matches = self.year_pattern.findall(normalized)
            results.update([match.strip() for match in year_matches])

            # Match context-based phrases
            if any(kw in normalized.lower() for kw in self.context_keywords):
                results.add(normalized)

        return sorted(results)

if __name__ == "__main__":
    jd_text = """
    We're looking for a Software Engineer with 3+ years of experience in backend development.
    Candidates should have a strong background in Python and REST APIs.
    Minimum of 5 years working in a fast-paced environment is preferred.
    Must have hands-on experience with cloud platforms like AWS or Azure.
    """

    extractor = JobExperienceExtractor()
    print(extractor.extract(jd_text))

