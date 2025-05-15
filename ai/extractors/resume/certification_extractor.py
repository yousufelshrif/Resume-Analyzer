"""
CertificationExtractor Module

This module defines the CertificationExtractor class, which extracts professional certifications 
from unstructured resume or profile text. It supports both exact matching from a known list of 
popular certifications and fuzzy pattern detection using keywords and acronyms.

Certifications are detected using:
- Predefined names like "AWS Certified", "PMP", "TensorFlow Developer"
- Common acronyms such as AZ-900, CCNA, CKA, PMP, etc.
- Fallback keywords like "certified", "exam", "badge", or "training"

Features:
    - Detect well-known certifications and credentials
    - Extract acronyms and training-related terms using regex
    - Optionally return full matching lines or just the detected names
    - Deduplicated and sorted output

Classes:
    CertificationExtractor: Extracts recognized or inferred certifications from resume text.
    
Dependencies:
    - re: for efficient regex matching
    - collections: for efficient data structures and operations
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume parsing and talent profiling
    - Automated recruiter pipelines
    - Certificate verification and enrichment
    - NLP processing for career platforms
"""


import re
from typing import List, Optional, Union


class CertificationExtractor:
    """
    A utility class to extract known and inferred certifications from resume text.

    This class uses pattern matching to detect popular certification names and acronyms, 
    while also using fallback keyword heuristics to catch less common credentials, badges, 
    and training references.

    Attributes:
        known_certs (List[str]): A list of predefined or custom known certifications to match against.

    Methods:
        extract(text: str, return_lines: bool = False) -> List[str]:
            Extracts and returns certifications or their source lines from resume text.
    """

    def __init__(self, known_certs: Optional[List[str]] = None):
        """
        Initialize the CertificationExtractor with a default or user-provided list of known certifications.

        Args:
            known_certs (Optional[List[str]]): List of certification names/acronyms to match against.
        """
        self.known_certs = known_certs or [
            "AWS Certified", "Google Cloud Certified", "Microsoft Certified", "Azure Fundamentals", "AZ-900",
            "Certified Scrum Master", "Scrum Master", "CompTIA A+", "CompTIA Security+", "CompTIA Network+",
            "Cisco Certified", "CCNA", "CKA", "CKAD", "Oracle Certified", "TOGAF", "ITIL", "CISSP",
            "Adobe Certified", "PMP", "PRINCE2", "Coursera", "Udemy", "edX", "DataCamp", "Trailhead",
            "IBM Data Science", "TensorFlow Developer", "Deep Learning Specialization", "Salesforce Certified",
            "LinkedIn Skill Assessment", "Superbadge", "Kubernetes Mastery", "AI For Everyone", "OCI Architect",
            "Google Cloud Professional", "Microsoft Azure Fundamentals", "OCI 2023 Architect Associate",
            "Certified Kubernetes Administrator"
        ]
        self.fallback_pattern = re.compile(
            r"(cert(ification|ified)|cert\.|badge|exam|track|specialization|credential|training|academy)",
            re.IGNORECASE
        )
        self.acronym_pattern = re.compile(r'\b(AZ-\d{3}|CKA|CKAD|CSM|PMP|CCNA|OCI|CKS|ITIL)\b')

    def extract(self, text: str, return_lines: bool = False) -> List[str]:
        """
        Extract certifications from resume text.

        Args:
            text (str): Raw resume content.
            return_lines (bool): If True, return the full matching lines. Otherwise, return only matched certification names.

        Returns:
            List[str]: Sorted and deduplicated list of certification names or source lines.
        """
        if not text or not isinstance(text, str):
            return []

        lines = [line.strip("•-–—•* ") for line in text.split('\n') if line.strip()]
        results = set()

        for line in lines:
            normalized = re.sub(r'[^\w\s\-#@.:/()]', '', line).strip()
            matched = False

            # Match known certifications
            for cert in self.known_certs:
                if cert.lower() in normalized.lower():
                    results.add(line if return_lines else cert)
                    matched = True
                    break

            # Match common acronyms
            if not matched:
                acronyms = self.acronym_pattern.findall(normalized)
                for acr in acronyms:
                    results.add(line if return_lines else acr)
                    matched = True

            # Fallback keyword-based match
            if not matched and self.fallback_pattern.search(normalized):
                results.add(line)

        return sorted(results)
