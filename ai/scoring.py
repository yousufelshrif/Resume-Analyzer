import os
import sys
from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util

# Get the absolute path of the project root directory (parent of 'ai' directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import extractors
from extractors.resume.resume_extractor import ResumeExtractor
from extractors.job.job_extractor import JobExtractor

# Load SBERT model once at the beginning
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

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
        "Skills": 0.55,
        "Certifications": 0.35,
        "Languages": 0.1
    }

    # Compute individual field scores
    skills_score = compute_skills_score(resume_data.get("Skills", []), job_data.get("Skills", []))
    certs_score = compute_certifications_score(resume_data.get("Certifications", []), job_data.get("Certifications", []))
    lang_score = compute_languages_score(resume_data.get("Languages", []), job_data.get("Languages", []))

    # Compute weighted average
    total_score = (
        skills_score * weights["Skills"] +
        certs_score * weights["Certifications"] +
        lang_score * weights["Languages"]
    ) * 100  # Scale to 0-100

    return total_score

def compute_skills_score(resume_skills: list, job_skills: list) -> float:
    """Calculate score based on exact skill matches."""
    if not job_skills:
        return 1.0
    matching_skills = set(resume_skills).intersection(set(job_skills))
    return len(matching_skills) / len(job_skills)

def compute_certifications_score(resume_certs: list, job_certs: list) -> float:
    """Calculate score based on exact certification matches."""
    if not job_certs:
        return 1.0
    matching_certs = set(resume_certs).intersection(set(job_certs))
    return len(matching_certs) / len(job_certs)


def compute_languages_score(resume_langs: list, job_langs: list) -> float:
    """Calculate score based on exact language matches."""
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

    # Languages feedback
    missing_langs = set(job_data.get("Languages", [])) - set(resume_data.get("Languages", []))
    feedback["Languages"] = f"Missing languages: {', '.join(missing_langs)}" if missing_langs else "Languages meet job requirements."

    return feedback

# Example usage
if __name__ == "__main__":
    resume_text = """
    Ahmed Mostafa
Senior Software Engineer | Backend & ML Specialist
Cairo, Egypt | ahmed.dev[at]gmail[dot]com | +20 100 123 4567 | linkedin.com/in/ahmedmostafa | github.com/ahmeddev

Summary:
Results-driven backend engineer with 6+ years of experience designing scalable systems using Python, FastAPI, PostgreSQL, and Docker. Proficient in building machine learning pipelines, deploying models to production with MLflow and Streamlit. Strong advocate for clean code, CI/CD, and agile development.

Skills:
- Programming: Python, JavaScript, SQL, C++
- ML/AI: Scikit-learn, PyTorch, Transformers, XGBoost, Hugging Face, LangChain
- Web: FastAPI, Flask, Django, React, Next.js, Tailwind CSS
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- DevOps: Docker, Kubernetes, GitHub Actions, Terraform, AWS, GCP
- Tools: Jupyter, VS Code, Git, Postman, Slack, Notion
- Soft Skills: Problem Solving, Teamwork, Communication, Leadership, Critical Thinking

Experience:
Senior Backend Engineer – DataStack AI (Remote)
Aug 2021 – Present
- Built a scalable FastAPI backend for a recommendation engine with PostgreSQL & Redis.
- Containerized applications using Docker and deployed to GCP with Kubernetes.
- Developed automated CI/CD pipelines using GitHub Actions.
- Collaborated cross-functionally with frontend and ML teams using Agile.

Machine Learning Engineer – TechNova Labs
Jan 2019 – Jul 2021
- Deployed NLP models for resume parsing and classification using Hugging Face Transformers.
- Trained and tuned models with Scikit-learn, PyTorch, and MLflow.
- Developed an interactive data dashboard with Streamlit and Plotly.

Education:
Bachelor of Computer Science, Cairo University, 2018
GPA: 3.7 / 4.0

Certifications:
- AWS Certified Solutions Architect (2023–2026)
- Google Cloud Professional ML Engineer
- Microsoft Azure Fundamentals (AZ-900)
- Deep Learning Specialization – Coursera (Andrew Ng)
- ITIL v4 Foundation
- Certified Kubernetes Administrator (CKA)

Projects:
AI Resume Analyzer
- Built a Streamlit app that extracts and analyzes resume data using NLP and BERT NER.
- Features: skill matching, email & phone extraction, certification parser.

E-commerce REST API
- Designed a secure REST API using Django REST Framework.
- Integrated Stripe payments and user authentication with JWT.

Languages:
- Arabic (Native)
- English (Fluent)
- German (Intermediate)

Interests:
- Open source contributions
- AI ethics & fairness
- Playing chess & learning languages

    """

    job_text = """
    About the job
Introduction

In this role, you'll work in one of our IBM Consulting Client Innovation Centers (Delivery Centers), where we deliver deep technical and industry expertise to a wide range of public and private sector clients around the world. Our delivery centers offer our clients locally based skills and technical expertise to drive innovation and adoption of new technology.

A career in IBM Consulting is rooted by long-term relationships and close collaboration with clients across the globe.

You'll work with visionaries across multiple industries to improve the hybrid cloud and AI journey for the most innovative and valuable companies in the world. Your ability to accelerate impact and make meaningful change for your clients is enabled by our strategic partner ecosystem and our robust technology platforms across the IBM portfolio; including Software and Red Hat.

Curiosity and a constant quest for knowledge serve as the foundation to success in IBM Consulting. In your role, you'll be encouraged to challenge the norm, investigate ideas outside of your role, and come up with creative solutions resulting in ground breaking impact for a wide network of clients. Our culture of evolution and empathy centers on long-term career growth and development opportunities in an environment that embraces your unique skills and experience.

Your Role And Responsibilities

We are seeking an experienced Data Scientist. The ideal candidate will have a deep understanding of Machine Learning, Generative AI, and Large Language Models, combined with strong leadership abilities. This role will be responsible for business development, overseeing the development and implementation of advanced data-driven solutions as well as mentor a team of talented data scientists.

Technical Oversight

Oversee the design, development, and deployment of Machine Learning models and AI solutions.
Ensure the use of best practices in data science, including model validation, performance monitoring, and continuous improvement.
Stay informed about the latest developments in AI/ML and drive the adoption of relevant technologies within the team.

Team Development

Provide mentorship and professional development opportunities to project and practice team members.
Actively support in recruitment efforts to attract top talent and grow the team as needed.
Help Foster a culture of learning and continuous development within the AI/Data Science team.

Preferred Education

Master's Degree

Experience

Required technical and professional expertise

7+ years of experience in Data Science and Machine Learning with at least 1 year of experience in conversational solutions design and development using Watson Assistant or similar conversational AI platforms.
Proven track record of delivering AI/ML projects.
Experience with Generative AI and Large Language Models is highly desirable

Technical Skills

Proficiency in programming languages such as Python, R, or Scala.
Deep understanding of Machine Learning frameworks (e.g., TensorFlow, PyTorch) and data processing tools (e.g., SQL, Pandas).
Experience with cloud platforms (e.g., AWS, Azure, Google Cloud) and machine learning deployment.
Strong knowledge of Natural Language Processing (NLP) and AI ethics.

Leadership Skills

Leadership skills with the ability to inspire and motivate junior team members.
Strategic thinking with the ability to align data science initiatives with business objectives.
Very good communication skills, capable of conveying complex ideas to a variety of audiences.
Proven ability to work collaboratively in projects with cross-functional teams.
Experience in building/scaling data science teams and implementing AI solutions in a large (preferably, consulting) organization.
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