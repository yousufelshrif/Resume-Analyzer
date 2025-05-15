"""
ProjectExtractor Module

This module provides the ProjectExtractor class for extracting structured project information
from resume or CV text. It identifies project titles, associated descriptions, and optionally
extracts technologies or skills mentioned in each project using a pluggable skill extraction function.

Features:
    - Detects project section from standard headers like "Projects" or "Capstone"
    - Extracts project titles and descriptions from unstructured text
    - Optionally extracts technologies using a custom skill extraction function
    - Supports structured or raw output for further processing

Classes:
    ProjectExtractor: A class for extracting and structuring project blocks from resume text.
    
Dependencies:
    - re: for efficient regex matching
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume parsing and candidate enrichment
    - Automated career profile building
    - NLP pipelines for CV analysis
    - Custom ATS (Applicant Tracking System) tools
"""


import re
from typing import List, Optional, Callable, Dict


class ProjectExtractor:
    """
    A class to extract project entries from resume text.

    This class identifies project titles and associated descriptions in resumes,
    optionally extracting technology keywords using a custom skill extraction function.

    Attributes:
        known_skills (Optional[List[str]]): List of technologies/skills to detect in descriptions.
        extract_skills_fn (Optional[Callable[[str, List[str]], List[str]]]): 
            Optional skill extraction function used to extract technologies from project descriptions.
    """

    def __init__(
        self,
        known_skills: Optional[List[str]] = None,
        extract_skills_fn: Optional[Callable[[str, List[str]], List[str]]] = None
    ):
        """
        Initializes the ProjectExtractor.

        Args:
            known_skills (Optional[List[str]]): List of technology keywords to detect.
            extract_skills_fn (Optional[Callable]): Function to extract skills from a text block.
                Should take (text: str, skill_list: List[str]) and return List[str].
        """
        self.known_skills = known_skills or []
        self.extract_skills_fn = extract_skills_fn

        self.project_keywords = ["project", "projects", "personal project", "capstone"]
        self.stop_keywords = ["education", "experience", "certifications", "languages", "interests"]
        self.title_pattern = re.compile(r'^[A-Z][A-Za-z0-9\s\-\(\)]{3,40}$')

    def extract(self, text: str, return_structured: bool = True, max_lines: int = 10) -> List[Dict[str, str]]:
        """
        Extracts project information from resume text.

        Args:
            text (str): Resume full text.
            return_structured (bool): If True, return dicts with title, description, technologies.
            max_lines (int): Maximum lines to scan after the section header.

        Returns:
            List[Dict[str, str]]: List of extracted project dictionaries with:
                - 'Title': Project title
                - 'Description': Project summary text
                - 'Technologies': List of skills (if extract_skills_fn is provided)
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        project_start = None

        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in self.project_keywords):
                project_start = i + 1
                break

        if project_start is None:
            return []

        # Collect lines after the project section until a new section
        block = []
        for line in lines[project_start:]:
            if any(kw in line.lower() for kw in self.stop_keywords):
                break
            block.append(line)

        projects = []
        current = {"Title": None, "Description": [], "Technologies": []}

        for line in block:
            if self.title_pattern.match(line) and not line.startswith("-"):
                if current["Title"]:
                    if return_structured:
                        current["Description"] = " ".join(current["Description"]).strip()
                        if self.extract_skills_fn:
                            current["Technologies"] = self.extract_skills_fn(current["Description"], self.known_skills)
                        projects.append(current)
                    current = {"Title": None, "Description": [], "Technologies": []}
                current["Title"] = line
            else:
                current["Description"].append(line)

        if current["Title"]:
            current["Description"] = " ".join(current["Description"]).strip()
            if self.extract_skills_fn:
                current["Technologies"] = self.extract_skills_fn(current["Description"], self.known_skills)
            projects.append(current)

        return projects
