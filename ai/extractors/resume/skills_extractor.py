"""
SkillExtractor Module

This module provides the SkillExtractor class for extracting technical and soft skills
from unstructured text data such as resumes and job descriptions.

It supports skill frequency counting, category grouping, case preservation, 
minimum frequency filtering, and efficient precompiled regex matching. 
Skill categories can be customized or default to a comprehensive modern tech stack.

Classes:
    SkillExtractor: Extracts relevant skills from text based on predefined or user-supplied categories.
    
Dependencies:
    - re: for efficient regex matching
    - collections: for efficient data structures and operations
    - typing: for type hints and annotations

Typical Use Cases:
    - Resume screening and parsing
    - Job description analysis
    - HR automation tools
    - Career recommendation systems
"""

import re
from collections import defaultdict
from typing import Optional, Union, List, Dict

class SkillExtractor:
    """
    Extracts technical and soft skills from a resume or job description text using customizable skill categories.

    Attributes:
        skill_set (dict): A dictionary mapping skill categories to lists of skill keywords.
    """

    def __init__(self, skill_set: Optional[dict] = None):
        """
        Initialize the SkillExtractor with an optional custom skill set.

        Args:
            skill_set (dict, optional): A dictionary mapping categories to skill keywords.
                If not provided, default categories and skills will be used.
        """
        self.skill_set = skill_set or self._default_skills()
        
        
    def _default_skills(self) -> dict:
        """Returns the default skill categories and keywords."""
        return {
            "Programming Languages": [
                "Python", "Java", "JavaScript", "JS", "TypeScript", "C++", "C#", "SQL", "R", "Go", "Rust",
                "Scala", "Perl", "Ruby", "Dart", "Objective-C", "Swift", "Kotlin"
            ],
            "AI / ML / NLP": [
                "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "XGBoost", "LightGBM", "CatBoost",
                "Machine Learning", "ML", "Deep Learning", "DL", "NLP", "LLM",
                "Transformers", "Hugging Face", "LangChain", "OpenAI API", "RAG", "Prompt Engineering",
                "LLM Fine-tuning", "AutoML", "spaCy", "NLTK", "BERT", "GPT", "Llama", "Claude",
                "FAISS", "ChromaDB", "Weaviate", "Haystack", "H2O.ai", "Vertex AI"
            ],
            "Web Development": [
                "HTML", "CSS", "SASS", "LESS", "Tailwind CSS", "Bootstrap", "Material-UI", "Chakra UI",
                "React", "Next.js", "Vue.js", "Angular", "Node.js", "Express", "Django", "Flask",
                "FastAPI", "ASP.NET", "Laravel", "Ruby on Rails", "REST API", "GraphQL", "WebSockets",
                "tRPC", "Zustand", "Redux", "React Query", "Vite", "Webpack", "Parcel", "Babel"
            ],
            "Cloud & DevOps": [
                "AWS", "Azure", "GCP", "DigitalOcean", "Heroku", "Vercel", "Netlify",
                "Docker", "Kubernetes", "Helm", "Terraform", "Ansible", "Pulumi", "CloudFormation",
                "GitHub Actions", "GitLab CI/CD", "Jenkins", "CircleCI", "ArgoCD",
                "Linux", "Bash", "Shell Scripting", "Serverless", "Prometheus", "Grafana", "Istio"
            ],
            "Databases": [
                "MySQL", "PostgreSQL", "MongoDB", "SQLite", "BigQuery", "Snowflake", "Oracle", "SQL Server",
                "Redis", "Firestore", "Cassandra", "DynamoDB", "InfluxDB", "MariaDB", "Redshift",
                "Neo4j", "Supabase", "ElasticSearch", "DuckDB"
            ],
            "Visualization & BI": [
                "Power BI", "Tableau", "Looker", "Google Data Studio", "Plotly", "Dash",
                "Matplotlib", "Seaborn", "D3.js", "Grafana", "Apache Superset", "Metabase"
            ],
            "Soft Skills": [
                "Communication", "Problem Solving", "Leadership", "Teamwork", "Adaptability",
                "Strategic Thinking", "Attention to Detail", "Time Management", "Creativity",
                "Critical Thinking", "Collaboration", "Decision Making", "Self-Motivation",
                "Work Ethic", "Conflict Resolution", "Public Speaking", "Presentation Skills",
                "Mentoring", "Accountability", "Customer Focus", "Project Management",
                "Empathy", "Emotional Intelligence"
            ]
        }
        

    def extract_skills(
        self,
        text: str,
        return_freq: bool = False,
        return_grouped: bool = False
    ) -> Union[List[str], Dict[str, Union[int, List[str]]], None]:
        """
        Extract skills from a given text based on the provided or default skill set.

        Args:
            text (str): The input resume or job description text.
            return_freq (bool): If True, returns a dictionary with skill frequencies.
            return_grouped (bool): If True, returns a dictionary grouping skills by category.

        Returns:
            Union[List[str], Dict[str, Union[int, List[str]]], None]:
                - If return_grouped is True: Dictionary grouped by category with matched skills.
                - If return_freq is True: Dictionary with skill name as key and frequency as value.
                - Otherwise: List of matched skill names.
        """
        text = text.lower()
        skills_found = defaultdict(list if return_grouped else int)

        for category, skills in self.skill_set.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                matches = re.findall(pattern, text)
                if matches:
                    if return_grouped:
                        skills_found[category].append(skill)
                    elif return_freq:
                        skills_found[skill] += len(matches)
                    else:
                        skills_found[skill] = 1

        if return_grouped:
            return {k: sorted(set(v)) for k, v in skills_found.items() if v}
        elif return_freq:
            return dict(sorted(skills_found.items(), key=lambda x: -x[1]))
        else:
            return sorted(skills_found.keys()) if skills_found else None
