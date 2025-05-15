"""
JobCertificationExtractor Module

This module provides the JobCertificationExtractor class, which is used to identify
certifications and credentials mentioned in a job description. It supports detection of:

- Known certification names (e.g., "AWS Certified", "PMP", "TensorFlow Developer")
- Common acronyms (e.g., AZ-900, CKAD, CCNA)
- Fallback keyword-based matches (e.g., lines containing "certified", "training", or "badge")

The extractor works on unstructured text input and uses pattern matching and regex heuristics
to return a deduplicated list of relevant certification-related mentions.

Classes:
    JobCertificationExtractor: Extracts known or inferred certifications from job description text.

Typical Use Cases:
    - Job description parsing
    - Skill gap analysis
    - Automated job matching and ranking
    - Recruiter and HR automation systems
"""


import re
from typing import List, Optional


class JobCertificationExtractor:
    """
    A class to extract certifications mentioned in a job description.

    It detects known certification names and acronyms using pattern matching,
    and also supports heuristic keyword-based discovery of training or credential-related phrases.

    Attributes:
        known_certs (List[str]): List of known or industry-recognized certifications.
    """

    def __init__(self, known_certs: Optional[List[str]] = None):
        """
        Initializes the extractor with an optional list of known certifications.

        Args:
            known_certs (Optional[List[str]]): Custom certification names or acronyms.
        """
        self.known_certs = known_certs or [
            "AWS Certified", "Google Cloud Certified", "Microsoft Certified", "Azure Fundamentals", "AZ-900",
            "Certified Scrum Master", "Scrum Master", "CompTIA A+", "CompTIA Security+", "CompTIA Network+",
            "Cisco Certified", "CCNA", "CKA", "CKAD", "Oracle Certified", "TOGAF", "ITIL", "CISSP",
            "Adobe Certified", "PMP", "PRINCE2", "Coursera", "Udemy", "edX", "DataCamp", "Trailhead",
            "IBM Data Science", "TensorFlow Developer", "Deep Learning Specialization", "Salesforce Certified",
            "Kubernetes Mastery", "AI For Everyone", "OCI Architect", "Google Cloud Professional",
            "Microsoft Azure Fundamentals", "Certified Kubernetes Administrator"
        ]

        self.fallback_pattern = re.compile(
            r"(cert(ification|ified)|cert\.|badge|exam|track|specialization|credential|training|academy|licensed)",
            re.IGNORECASE
        )

        self.acronym_pattern = re.compile(r'\b(AZ-\d{3}|CKA|CKAD|CSM|PMP|CCNA|OCI|CKS|ITIL|CISSP)\b')

    def extract(self, text: str) -> List[str]:
        """
        Extract certification names from a job description.

        Args:
            text (str): The full job description content.

        Returns:
            List[str]: A sorted list of deduplicated certifications or keywords found.
        """
        lines = [line.strip("•-–—* ") for line in text.split('\n') if line.strip()]
        results = set()

        for line in lines:
            normalized = re.sub(r'[^\w\s\-#@.:/()]', '', line).strip()
            matched = False

            # 1. Match known certs
            for cert in self.known_certs:
                if cert.lower() in normalized.lower():
                    results.add(cert)
                    matched = True
                    break

            # 2. Match common acronyms
            if not matched:
                acronyms = self.acronym_pattern.findall(normalized)
                results.update(acronyms)
                matched = bool(acronyms)

            # 3. Match general fallback cert/training/badge terms
            if not matched and self.fallback_pattern.search(normalized):
                results.add(line)

        return sorted(results)


if __name__ == "__main__":
    jd_text = """
    We are looking for a Cloud Engineer with relevant certifications.
    Preferred: AWS Certified Solutions Architect, Azure Fundamentals (AZ-900), or Google Cloud Professional.
    Bonus if you're a Certified Kubernetes Administrator (CKA) or have completed Coursera training.
    PMP certification is a plus.
    """

    extractor = JobCertificationExtractor()
    print(extractor.extract(jd_text))
