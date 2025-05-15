"""
JobEducationExtractor Module

This module provides the JobEducationExtractor class, which is used to identify
educational requirements and qualifications mentioned in a job description. It supports detection of:

- Degree levels (e.g., Bachelor's, Master's, PhD)
- Fields of study (e.g., Computer Science, Engineering)
- Required vs preferred qualifications
- Minimum education requirements
- Academic background requirements
- Educational experience levels
- Industry-specific education requirements

The extractor works on unstructured text input and uses pattern matching and regex heuristics
to return structured information about educational requirements.

Classes:
    JobEducationExtractor: Extracts educational requirements from job description text.
    EducationRequirement: Data class for structured education requirement information.

Typical Use Cases:
    - Job description parsing
    - Candidate-job education matching
    - Automated job matching and ranking
    - Recruiter and HR automation systems
"""

import re
import logging
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EducationRequirement:
    """
    Data class to hold structured education requirement information.
    
    Attributes:
        degree_level (str): The degree level (e.g., "Bachelor's", "Master's")
        field_of_study (Optional[str]): The field of study (e.g., "Computer Science")
        is_required (bool): Whether the education is required or preferred
        confidence (float): Confidence score for the extraction
        context (Optional[str]): Surrounding text context
        priority (Optional[str]): Priority level (e.g., "required", "preferred", "plus")
        minimum_years (Optional[int]): Minimum years of education required
        industry_specific (bool): Whether the requirement is industry-specific
        gpa_requirement (Optional[float]): Required GPA if specified
        honors_required (List[str]): Required honors or achievements
        institution_type (Optional[str]): Type of institution required
        accreditation (Optional[str]): Required accreditation
    """
    degree_level: str
    field_of_study: Optional[str]
    is_required: bool
    confidence: float
    context: Optional[str] = None
    priority: Optional[str] = None
    minimum_years: Optional[int] = None
    industry_specific: bool = False
    gpa_requirement: Optional[float] = None
    honors_required: List[str] = None
    institution_type: Optional[str] = None
    accreditation: Optional[str] = None

class JobEducationExtractor:
    """
    A class to extract educational requirements from job descriptions.

    Features:
        - Degree level detection
        - Field of study identification
        - Required vs preferred analysis
        - Priority level detection
        - Context extraction
        - Confidence scoring
        - Industry-specific requirements
        - Minimum education requirements
        - GPA requirements
        - Honors requirements
        - Institution type requirements
        - Accreditation requirements
    """

    def __init__(self):
        """Initialize the JobEducationExtractor with necessary patterns and keywords."""
        # Degree normalization mapping
        self.degree_normalization = {
            # Undergraduate degrees
            r'\bBachelor(?:\'s)?\b': 'bachelor',
            r'\bB\.S\.\b': 'bachelor',
            r'\bB\.A\.\b': 'bachelor',
            r'\bB\.E\.\b': 'bachelor',
            r'\bB\.Tech\b': 'bachelor',
            r'\bBBA\b': 'bachelor',
            r'\bB\.Com\b': 'bachelor',
            r'\bBFA\b': 'bachelor',
            
            # Graduate degrees
            r'\bMaster(?:\'s)?\b': 'master',
            r'\bM\.S\.\b': 'master',
            r'\bM\.A\.\b': 'master',
            r'\bM\.E\.\b': 'master',
            r'\bM\.Tech\b': 'master',
            r'\bMBA\b': 'master',
            r'\bMFA\b': 'master',
            r'\bM\.Com\b': 'master',
            
            # Doctoral degrees
            r'\bPhD\b': 'doctoral',
            r'\bPh\.D\b': 'doctoral',
            r'\bDoctorate\b': 'doctoral',
            r'\bDoctor\b': 'doctoral',
            r'\bD\.Sc\b': 'doctoral',
            r'\bD\.Litt\b': 'doctoral'
        }

        # Education level mapping
        self.degree_levels = {
            'bachelor': 'undergraduate',
            'master': 'graduate',
            'doctoral': 'doctoral'
        }

        # Priority indicators
        self.priority_indicators = {
            "required": [
                "required", "must have", "mandatory", "essential",
                "prerequisite", "minimum requirement", "must be",
                "must hold", "must possess", "must demonstrate"
            ],
            "preferred": [
                "preferred", "desired", "nice to have", "should have",
                "recommended", "ideal", "should be", "should hold",
                "should possess", "should demonstrate", "plus",
                "bonus", "advantage", "additional", "extra"
            ]
        }

        # Common fields of study
        self.fields_of_study = {
            "Computer Science": [
                "Computer Science", "CS", "Computing", "Software Engineering",
                "Computer Engineering", "Information Technology", "IT",
                "Computer Systems", "Computing Science", "Information Systems"
            ],
            "Engineering": [
                "Engineering", "Mechanical Engineering", "Electrical Engineering",
                "Civil Engineering", "Chemical Engineering", "Industrial Engineering",
                "Aerospace Engineering", "Biomedical Engineering", "Computer Engineering",
                "Software Engineering", "Systems Engineering"
            ],
            "Data Science": [
                "Data Science", "Data Analytics", "Machine Learning",
                "Artificial Intelligence", "AI", "ML", "Statistics",
                "Applied Mathematics", "Computational Science", "Big Data"
            ],
            "Business": [
                "Business", "Business Administration", "Management",
                "Finance", "Marketing", "Economics", "Accounting",
                "Business Analytics", "Business Intelligence", "Entrepreneurship"
            ]
        }

    def extract(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract educational requirements from a job description.

        Args:
            text (str): The job description text.

        Returns:
            Dict[str, List[Dict]]: Dictionary containing list of education requirements in the specified format.
        """
        try:
            if not text:
                logger.warning("Empty text provided")
                return {"education": []}

            requirements = []
            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Extract degree information
                degree_info = self._extract_degree_info(line)
                if not degree_info:
                    continue

                # Extract field of study
                field_of_study = self._extract_field_of_study(line)
                
                # Determine if required or preferred
                required, preferred = self._determine_requirement_status(line)

                # Create education requirement entry
                requirement = {
                    "degree": degree_info['degree'],
                    "normalized_degree": degree_info['normalized_degree'],
                    "field_of_study": field_of_study,
                    "normalized_field": field_of_study.lower() if field_of_study else None,
                    "institution": None,
                    "location": None,
                    "start_date": None,
                    "end_date": None,
                    "grade": None,
                    "level": degree_info['level'],
                    "required": required,
                    "preferred": preferred,
                    "confidence": degree_info['confidence'],
                    "source": "job_description",
                    "context": line
                }
                
                requirements.append(requirement)

            return {"education": requirements}

        except Exception as e:
            logger.error(f"Error extracting education requirements: {str(e)}")
            return {"education": []}

    def _extract_degree_info(self, line: str) -> Optional[Dict]:
        """Extract degree information with confidence scoring and normalization."""
        line_lower = line.lower()
        
        # Find normalized degree
        normalized_degree = None
        degree = None
        
        for pattern, norm in self.degree_normalization.items():
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                normalized_degree = norm
                degree = match.group(0)
                break
        
        if not normalized_degree:
            return None

        # Calculate confidence based on context
        confidence = 1.0
        
        # Reduce confidence for very short lines
        if len(line) < 10:
            confidence *= 0.5
            
        # Increase confidence for clear degree mentions
        if "degree" in line_lower or "in" in line_lower:
            confidence += 0.1
            
        # Increase confidence for field of study mention
        if any(field.lower() in line_lower for fields in self.fields_of_study.values() for field in fields):
            confidence += 0.1

        return {
            "degree": degree,
            "normalized_degree": normalized_degree,
            "level": self.degree_levels.get(normalized_degree, "unknown"),
            "confidence": min(1.0, confidence)
        }

    def _extract_field_of_study(self, line: str) -> Optional[str]:
        """Extract field of study from the line."""
        line_lower = line.lower()
        
        for field, patterns in self.fields_of_study.items():
            for pattern in patterns:
                if pattern.lower() in line_lower:
                    return field
        return None

    def _determine_requirement_status(self, line: str) -> Tuple[bool, bool]:
        """Determine if the education is required or preferred."""
        line_lower = line.lower()
        
        required = False
        preferred = False
        
        # Check for required indicators
        if any(indicator in line_lower for indicator in self.priority_indicators["required"]):
            required = True
        # Check for preferred indicators
        elif any(indicator in line_lower for indicator in self.priority_indicators["preferred"]):
            preferred = True
            
        return required, preferred

def main():
    """
    Main function demonstrating the JobEducationExtractor capabilities.
    """
    sample_job_description = """
    Required Qualifications:
    - Bachelor's degree in Computer Science or related field
    - Minimum 4 years of relevant experience
    - Strong background in Software Engineering

    Preferred Qualifications:
    - Master's degree in Computer Science or Engineering
    - PhD in Artificial Intelligence or Machine Learning would be a plus
    - Additional certification in Cloud Computing is preferred
    """

    extractor = JobEducationExtractor()
    
    print("\n=== Job Education Requirements Analysis ===\n")
    
    result = extractor.extract(sample_job_description)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

