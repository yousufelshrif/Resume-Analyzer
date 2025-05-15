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
            "Microsoft Azure Fundamentals", "Certified Kubernetes Administrator",
            # Add Power Platform certifications
            "PL-100", "Power Platform App Maker",
            "PL-200", "Power Platform Functional Consultant",
            "PL-400", "Power Platform Developer",
            "PL-600", "Power Platform Solution Architect"
        ]

        # Pattern for certification codes like PL-100, PL-200, etc.
        self.cert_code_pattern = re.compile(r'\b(PL-\d{3})\b')
        
        # Pattern for certification names
        self.cert_name_pattern = re.compile(
            r'(?:certified|certification|cert\.|badge|exam|track|specialization|credential|training|academy|licensed)',
            re.IGNORECASE
        )

    def extract(self, text: str) -> List[str]:
        """
        Extract certification names from a job description.

        Args:
            text (str): The full job description content.

        Returns:
            List[str]: A sorted list of deduplicated certifications found.
        """
        results = set()
        
        # Split text into lines and process each line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Look for certification codes
            cert_codes = self.cert_code_pattern.findall(line)
            if cert_codes:
                results.update(cert_codes)
                continue

            # Look for known certifications
            for cert in self.known_certs:
                if cert.lower() in line.lower():
                    results.add(cert)
                    break

            # Look for lines containing certification-related keywords
            if self.cert_name_pattern.search(line):
                # Clean up the line and add it if it's not too long
                cleaned = re.sub(r'[^\w\s\-#@.:/()]', '', line).strip()
                if len(cleaned) < 100:  # Avoid adding entire paragraphs
                    results.add(cleaned)

        return sorted(list(results))


if __name__ == "__main__":
    jd_text = """
    We are looking for a Cloud Engineer with relevant certifications.
    Preferred: AWS Certified Solutions Architect, Azure Fundamentals (AZ-900), or Google Cloud Professional.
    Bonus if you're a Certified Kubernetes Administrator (CKA) or have completed Coursera training.
    PMP certification is a plus.
    Required: PL-100, PL-200 certifications.
    """

    extractor = JobCertificationExtractor()
    print(extractor.extract(jd_text))
