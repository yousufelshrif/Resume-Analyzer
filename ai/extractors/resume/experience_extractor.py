"""
ExperienceExtractor Module

This module provides the ExperienceExtractor class for parsing structured work experience
entries from raw resume text. It detects the "Experience" section by scanning for common 
section headers and extracts key components such as:

- Job Title
- Company Name
- Employment Dates
- Bullet-point Descriptions
- Raw Matched Line

The parser uses regex patterns to match title-company formats and date ranges, and stops 
at common section boundaries such as "Education" or "Certifications".

Classes:
    ExperienceExtractor: Extracts structured experience blocks from resume content.

Dependencies:
    - re: for efficient regex matching
    - typing: for type hints and annotations
"""


import re
from typing import List, Dict


class ExperienceExtractor:
    """
    A class to extract structured work experience entries from unstructured resume text.

    This extractor identifies the "Experience" section by matching common section headers 
    like 'Work History' or 'Employment', and parses the content to extract job titles, companies, 
    employment dates, and bullet-point descriptions.

    Methods:
        extract(text: str, max_lines: int = 40) -> List[Dict[str, str]]:
            Extracts experience entries from resume text.
    """

    def __init__(self):
        self.section_keywords = [
            "experience", "work history", "employment", "professional background"
        ]
        self.stop_keywords = ["education", "certification", "project"]
        self.title_company_pattern = re.compile(
            r'^(?P<title>[A-Za-z\s/()\-]+?)\s+[-–]\s+(?P<company>.+)$'
        )
        self.date_pattern = re.compile(r'(\b\d{4}\b).{0,5}(\bPresent\b|\b\d{4}\b)', re.IGNORECASE)

    def extract(self, text: str, max_lines: int = 40) -> List[Dict[str, str]]:
        """
        Extract structured work experience entries from resume text.

        Args:
            text (str): The full resume text to parse.
            max_lines (int): Maximum number of lines to scan below the experience header.

        Returns:
            List[Dict[str, str]]: A list of experience entries with keys: Title, Company, Date, Description, Raw.
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        experience_section = []
        section_found = False

        # Locate the start of the experience section
        for i, line in enumerate(lines):
            if not section_found and any(k in line.lower() for k in self.section_keywords):
                experience_section = lines[i + 1: i + 1 + max_lines]
                section_found = True
                break

        if not experience_section:
            return []

        experiences = []
        current = {}
        buffer = []

        for line in experience_section:
            if any(stop in line.lower() for stop in self.stop_keywords):
                break  # Stop when reaching a new section

            # Detect job title - company line
            tc_match = self.title_company_pattern.match(line)
            date_match = self.date_pattern.search(line)

            if tc_match:
                # Save previous job
                if current:
                    current["Description"] = " ".join(buffer).strip() if buffer else None
                    experiences.append(current)
                    buffer = []

                current = {
                    "Title": tc_match.group("title").strip(),
                    "Company": tc_match.group("company").strip(),
                    "Date": None,
                    "Raw": line
                }

            elif date_match and current:
                current["Date"] = date_match.group(0)

            elif line.startswith("-"):
                buffer.append(line)

        # Final flush
        if current:
            current["Description"] = " ".join(buffer).strip() if buffer else None
            experiences.append(current)

        return experiences
