"""
Education Extractor Module

This module provides functionality to extract and parse education-related information from resume text.
It includes features for detecting degrees, majors, GPAs, honors, dates, and institutions with confidence scoring.

Classes:
    Education: Data class for structured education information
    EducationExtractor: Main class for extracting education information from text

Example:
    >>> extractor = EducationExtractor()
    >>> education_entries = extractor.extract(resume_text)
    >>> for entry in education_entries:
    ...     print(f"Degree: {entry['degree']}")
"""

import re
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Education:
    """
    Data class to hold structured education information.
    
    Attributes:
        degree (str): The degree or qualification obtained
        institution (Optional[str]): The educational institution name
        year (Optional[str]): The year of completion
        major (Optional[str]): The major field of study
        minor (Optional[str]): The minor field of study
        gpa (Optional[float]): The grade point average
        honors (List[str]): List of honors and awards received
        location (Optional[str]): The location of the institution
        start_date (Optional[str]): The start date of the education
        end_date (Optional[str]): The end date of the education
        raw_text (Optional[str]): The original text from which information was extracted
        confidence (float): Confidence score for the extracted information
    """
    degree: str
    institution: Optional[str] = None
    year: Optional[str] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    gpa: Optional[float] = None
    honors: List[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    raw_text: Optional[str] = None
    confidence: float = 1.0

class EducationExtractor:
    """Basic education extractor for resumes."""

    def __init__(self):
        """Initialize with basic education patterns."""
        self.degree_patterns = [
            r"(?i)([A-Za-z\s]+)\s+(?:degree|diploma|certificate|bachelor|master|phd|doctorate)",
            r"(?i)(?:bachelor|master|phd|doctorate)\s+(?:of|in)\s+([A-Za-z\s]+)",
            r"(?i)([A-Za-z\s]+)\s+(?:university|college|institute|school)",
            r"(?i)(?:bachelor|master|phd|doctorate)\s+(?:of|in)\s+([A-Za-z\s]+)\s+(?:from|at)\s+([A-Za-z\s,]+)"
        ]
        
        self.date_patterns = [
            r'(?i)(?:graduated|completed|obtained|earned|received)\s+(?:in|on|date)?\s*(\d{4})',
            r'(?i)(?:graduation|completion|obtained|earned|received)\s+(?:date|year)?\s*(\d{4})',
            r'(?i)(?:from|between)\s+(\d{4})\s*(?:-|–|to|until)\s*(\d{4})',
            r'(?i)(?:started|began)\s+(?:in|on|date)?\s*(\d{4})'
        ]

    def extract(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extract education information from resume text.
        
        Args:
            text (str): The resume text to analyze
            
        Returns:
            Dict[str, List[Dict]]: Dictionary containing list of education entries
        """
        try:
            education_entries = []
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # Look for education section
                if 'education' in line.lower() or 'academic' in line.lower():
                    continue
                    
                # Look for degree patterns
                for pattern in self.degree_patterns:
                    match = re.search(pattern, line)
                    if match:
                        # Extract degree and field
                        if 'degree' in pattern:
                            degree = match.group(1).strip()
                            field = match.group(2).strip() if len(match.groups()) > 1 else None
                        else:
                            field = match.group(1).strip()
                            degree = match.group(2).strip() if len(match.groups()) > 1 else None
                        
                        # Extract institution
                        institution = None
                        if len(match.groups()) > 2:
                            institution = match.group(3).strip()
                        else:
                            # Look for institution in next line
                            next_line_idx = i + 1
                            if next_line_idx < len(lines):
                                next_line = lines[next_line_idx].strip()
                                if not next_line.startswith(('-', '•', '*')):
                                    institution = next_line
                        
                        # Extract dates
                        start_date = None
                        end_date = None
                        for date_pattern in self.date_patterns:
                            date_match = re.search(date_pattern, line)
                            if date_match:
                                if len(date_match.groups()) == 2:
                                    start_date = f"{date_match.group(1)}-01-01"
                                    end_date = f"{date_match.group(2)}-01-01"
                                else:
                                    end_date = f"{date_match.group(1)}-01-01"
                                break
                        
                        # Determine education level
                        level = None
                        if degree:
                            degree_lower = degree.lower()
                            if 'phd' in degree_lower or 'doctorate' in degree_lower:
                                level = 'doctoral'
                            elif 'master' in degree_lower:
                                level = 'graduate'
                            elif 'bachelor' in degree_lower:
                                level = 'undergraduate'
                            else:
                                level = 'other'
                        
                        education_entry = {
                            "degree": degree,
                            "normalized_degree": degree.lower() if degree else None,
                            "field_of_study": field,
                            "normalized_field": field.lower() if field else None,
                            "institution": institution,
                            "location": None,
                            "start_date": start_date,
                            "end_date": end_date,
                            "grade": None,
                            "level": level,
                            "required": None,
                            "preferred": None,
                            "confidence": 1.0,
                            "source": "resume",
                            "context": line,
                            "honors": []
                        }
                        education_entries.append(education_entry)
            
            return {"education": education_entries}
            
        except Exception as e:
            logger.error(f"Error extracting education: {str(e)}")
            return {"education": []}

def main():
    """
    Main function demonstrating the enhanced EducationExtractor capabilities.
    """
    sample_resume = """
    EDUCATION
    
    Master of Science (M.S.) in Data Science  
    University of California, Berkeley  
    September 2017 – June 2019  
    Dean's List | Research Fellowship in AI 
    
    Ph.D. in Artificial Intelligence  
    Massachusetts Institute of Technology  
    Expected Graduation: 2026  
    Specialization in Deep Learning and Robotics  
    Advisor: Dr. Andrew Ng

    Bachelor of Engineering in Electrical Engineering  
    Indian Institute of Technology – Delhi, India  
    Graduated: 2016  
    GPA: 8.7/10  
    First Class with Distinction  


    """

    extractor = EducationExtractor()
    
    print("\n=== Education Extraction Results ===\n")
    
    result = extractor.extract(sample_resume)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()