"""
JobSkillExtractor Module

This module defines the JobSkillExtractor class used to extract technical and soft skills
from unstructured job description text. It matches against predefined categories and allows
custom skill sets to support domain-specific needs.

Classes:
    JobSkillExtractor: Extracts skills from job descriptions, optionally grouped by category.

Typical Use Cases:
    - Parsing job descriptions for ATS/HR platforms
    - Matching job posts to candidate profiles
    - Highlighting required technical and soft skills
"""


import re
from typing import List, Dict, Optional, Union, Set


class JobSkillExtractor:
    """
    A class to extract relevant technical and soft skills from job descriptions.

    It matches skills across predefined categories such as Programming, AI/ML, Web Development,
    Cloud & DevOps, Databases, Visualization Tools, and Soft Skills. You can also pass a custom
    skill set.

    Attributes:
        skill_set (Dict[str, List[str]]): Dictionary of categorized skill keywords.
    """

    def __init__(self, skill_set: Optional[Dict[str, List[str]]] = None):
        """
        Initialize the extractor with a default or custom skill set.

        Args:
            skill_set (Optional[Dict[str, List[str]]]): Custom mapping of skill categories to skill terms.
        """
        self.skill_set = skill_set or {
            "Programming Languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "SQL", "Go", "Rust", "Kotlin", "Ruby"
            ],
            "AI / ML / NLP": [
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Keras",
                "NLP", "Transformer", "OpenAI", "LangChain", "spaCy", "LLM", "BERT", "GPT"
            ],
            "Web Development": [
                "HTML", "CSS", "React", "Next.js", "Angular", "Vue.js", "Node.js", "Express", "Flask", "Django"
            ],
            "Cloud & DevOps": [
                "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions"
            ],
            "Databases": [
                "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Oracle", "Firestore", "ElasticSearch"
            ],
            "Visualization & BI": [
                "Power BI", "Tableau", "Plotly", "Seaborn", "Matplotlib", "Looker"
            ],
            "Soft Skills": [
                "Communication", "Problem Solving", "Teamwork", "Adaptability", "Time Management",
                "Critical Thinking", "Leadership", "Creativity"
            ]
        }

    def extract(self, text: str, return_grouped: bool = False) -> Union[List[str], Dict[str, List[str]]]:
        """
        Extracts skills mentioned in a job description.

        Args:
            text (str): Raw job description content.
            return_grouped (bool): If True, return a dictionary grouped by skill category.

        Returns:
            Union[List[str], Dict[str, List[str]]]:
                - List of matched skill names (default)
                - Dictionary of matched skills grouped by category (if return_grouped=True)
        """
        text_lower = text.lower()
        skills_found: Union[Set[str], Dict[str, Set[str]]] = {} if return_grouped else set()

        for category, skills in self.skill_set.items():
            for skill in skills:
                pattern = rf"\b{re.escape(skill.lower())}\b"
                if re.search(pattern, text_lower):
                    if return_grouped:
                        skills_found.setdefault(category, set()).add(skill)
                    else:
                        skills_found.add(skill)

        if return_grouped:
            return {cat: sorted(list(skills)) for cat, skills in skills_found.items() if skills}
        else:
            return sorted(list(skills_found)) if skills_found else []
        
if __name__ == "__main__":
    jd_text = """
    We're looking for a backend engineer skilled in Python, Django, and PostgreSQL.
    Experience with AWS, Docker, and Kubernetes is preferred.
    Strong communication and problem-solving abilities are a must.
    """

    extractor = JobSkillExtractor()
    print(extractor.extract(jd_text))  # Flat list
    print(extractor.extract(jd_text, return_grouped=True))  # Grouped by category

