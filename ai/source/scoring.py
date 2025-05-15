import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname('__file__'), '..', '..'))
# Add the project root to Python path
sys.path.append(project_root)

# Now you can import from ai package
from ai.extractors.resume.resume_extractor import ResumeExtractor
from ai.extractors.job.job_extractor import JobExtractor
from typing import Dict, Any

def compute_matching_score(resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
    """
    Computes a matching score between resume and job description based on key fields.
    
    Args:
        resume_data (Dict[str, Any]): Parsed resume data from ResumeExtractor.
        job_data (Dict[str, Any]): Parsed job data from JobExtractor.
    
    Returns:
        float: Matching score between 0 and 100.
    """
    # Define weights for each field
    weights = {
        "Skills": 0.4,
        "Certifications": 0.2,
        "Education": 0.15,
        "Experience": 0.15,
        "Languages": 0.1
    }

    # Compute individual field scores
    skills_score = compute_skills_score(resume_data.get("Skills", []), job_data.get("Skills", []))
    certs_score = compute_certifications_score(resume_data.get("Certifications", []), job_data.get("Certifications", []))
    edu_score = compute_education_score(resume_data.get("Education", []), job_data.get("Education", []))
    exp_score = 0
    lang_score = compute_languages_score(resume_data.get("Languages", []), job_data.get("Languages", []))

    # Compute weighted average
    total_score = (
        skills_score * weights["Skills"] +
        certs_score * weights["Certifications"] +
        edu_score * weights["Education"] +
        exp_score * weights["Experience"] +
        lang_score * weights["Languages"]
    ) * 100  # Scale to 0-100

    return total_score

def compute_skills_score(resume_skills: list, job_skills: list) -> float:
    if not job_skills:
        return 1.0
    matching_skills = set(resume_skills).intersection(set(job_skills))
    return len(matching_skills) / len(job_skills)

def compute_certifications_score(resume_certs: list, job_certs: list) -> float:
    if not job_certs:
        return 1.0
    matching_certs = set(resume_certs).intersection(set(job_certs))
    return len(matching_certs) / len(job_certs)

def compute_education_score(resume_edu: list, job_edu: list) -> float:
    if not job_edu:
        return 1.0
    resume_edu_set = set(resume_edu)
    job_edu_set = set(job_edu)
    return 1.0 if job_edu_set.issubset(resume_edu_set) else 0.0

def compute_experience_score(resume_exp: list, job_exp: list) -> float:
    if not job_exp:
        return 1.0
    matching_exp = set(resume_exp).intersection(set(job_exp))
    return len(matching_exp) / len(job_exp)

def compute_languages_score(resume_langs: list, job_langs: list) -> float:
    if not job_langs:
        return 1.0
    matching_langs = set(resume_langs).intersection(set(job_langs))
    return len(matching_langs) / len(job_langs)

def generate_feedback(resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generates feedback based on differences between resume and job requirements.
    
    Args:
        resume_data (Dict[str, Any]): Parsed resume data.
        job_data (Dict[str, Any]): Parsed job data.
    
    Returns:
        Dict[str, str]: Feedback for each field.
    """
    feedback = {}

    # Skills feedback
    missing_skills = set(job_data.get("Skills", [])) - set(resume_data.get("Skills", []))
    feedback["Skills"] = f"Missing skills: {', '.join(missing_skills)}" if missing_skills else "All required skills present."

    # Certifications feedback
    missing_certs = set(job_data.get("Certifications", [])) - set(resume_data.get("Certifications", []))
    feedback["Certifications"] = f"Missing certifications: {', '.join(missing_certs)}" if missing_certs else "All required certifications present."

    # Education feedback
    if not set(job_data.get("Education", [])).issubset(set(resume_data.get("Education", []))):
        feedback["Education"] = "Education does not meet job requirements."
    else:
        feedback["Education"] = "Education meets job requirements."

    # Experience feedback
    missing_exp = set(job_data.get("Experience", [])) - set(resume_data.get("Experience", []))
    feedback["Experience"] = f"Missing experience: {', '.join(missing_exp)}" if missing_exp else "Experience meets job requirements."

    # Languages feedback
    missing_langs = set(job_data.get("Languages", [])) - set(resume_data.get("Languages", []))
    feedback["Languages"] = f"Missing languages: {', '.join(missing_langs)}" if missing_langs else "Languages meet job requirements."

    return feedback

# Example usage
if __name__ == "__main__":
    resume_text = """
    John Doe
    Email: john.doe@example.com
    Phone: +1 (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    GitHub: github.com/johndoe

    Skills:
    Python, JavaScript, React, FastAPI, Docker, SQL, Machine Learning

    Experience
    Software Engineer – OpenAI
    2021 – Present
    - Built RESTful APIs using FastAPI and deployed models on AWS
    - Collaborated on NLP models for document understanding

    Certifications
    AWS Certified Solutions Architect – Associate
    TensorFlow Developer Certificate

    Languages
    English, French, Arabic
    """

    job_text = """
    We're seeking a backend engineer with 3+ years of experience in Django and PostgreSQL.
    Required: Bachelor's degree in Computer Science or related field.
    Certifications like AWS Certified Solutions Architect or AZ-900 are a plus.
    Must be fluent in English and familiar with Docker, Kubernetes, and React.
    """

    # Parse resume and job description
    resume_extractor = ResumeExtractor()
    job_extractor = JobExtractor()

    resume_data = resume_extractor.parse(resume_text)
    job_data = job_extractor.parse(job_text)

    # Compute score
    score = compute_matching_score(resume_data, job_data)
    print(f"Matching Score: {score:.2f}/100")

    # Generate and print feedback
    feedback = generate_feedback(resume_data, job_data)
    for field, message in feedback.items():
        print(f"{field}: {message}")