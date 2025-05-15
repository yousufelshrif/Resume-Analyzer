"""
JobExtractor Module

This module defines the JobExtractor class, a unified interface that combines multiple
specialized extractors to parse and structure key requirements from unstructured
job descriptions.

It extracts:
- Required certifications
- Educational qualifications
- Years of experience and contextual experience phrases
- Technical and soft skills
- Language proficiency expectations

Each sub-extractor supports keyword matching and pattern recognition to handle
natural job description formats.

Classes:
    JobExtractor: Central interface for extracting structured job requirement components.
"""

from typing import Dict, Any

# Import specialized extractors
from .certification_extractor import JobCertificationExtractor
from .education_extractor import JobEducationExtractor
from .experience_extractor import JobExperienceExtractor
from .language_extractor import JobLanguageExtractor
from .skills_extractor import JobSkillExtractor


class JobExtractor:
    """
    JobExtractor class to aggregate all job requirement fields from a given job description.

    It leverages specialized extractor classes to return a structured dictionary of:
    - Certifications
    - Education requirements
    - Experience phrases
    - Skills
    - Languages
    """

    def __init__(self):
        self.cert_extractor = JobCertificationExtractor()
        self.edu_extractor = JobEducationExtractor()
        self.exp_extractor = JobExperienceExtractor()
        self.lang_extractor = JobLanguageExtractor()
        self.skill_extractor = JobSkillExtractor()

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parses the given job description text and returns extracted fields.

        Args:
            text (str): Raw job description content.

        Returns:
            Dict[str, Any]: Structured dictionary of extracted job requirements.
        """
        return {
            "Certifications": self.cert_extractor.extract(text),
            "Education": self.edu_extractor.extract(text),
            "Experience": self.exp_extractor.extract(text),
            "Skills": self.skill_extractor.extract(text),
            "Languages": self.lang_extractor.extract(text)
        }


if __name__ == "__main__":
    jd_text = """
    We're seeking a backend engineer with 3+ years of experience in Django and PostgreSQL.
    Required: Bachelor's degree in Computer Science or related field.
    Certifications like AWS Certified Solutions Architect or AZ-900 are a plus.
    Must be fluent in English and familiar with Docker, Kubernetes, and React.
    """

    extractor = JobExtractor()
    parsed = extractor.parse(jd_text)

    for key, value in parsed.items():
        print(f"{key}: {value}")
