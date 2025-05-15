from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models.job_description_model import JobDescription
from ...ai.extractors.job.job_extractor import JobExtractor
import json


def extract_job_description(text: str) -> Dict[str, Any]:
    """
    Extract structured job description information from raw text.

    Args:
        text (str): The full job description content.

    Returns:
        Dict[str, Any]: Parsed fields including skills, education, experience, etc.
    """
    extractor = JobExtractor()
    parsed = extractor.parse(text)

    def to_json(value: Any) -> str | None:
        if value is None:
            return None
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return None

    job_data: Dict[str, Any] = {
        "raw_text": text,
        "required_skills": to_json(parsed.get("Skills")),
        "required_education": to_json(parsed.get("Education")),
        "required_experience": to_json(parsed.get("Experience")),
        "required_certifications": to_json(parsed.get("Certifications")),
        "required_languages": to_json(parsed.get("Languages")),
    }

    return job_data


def save_job_description(db: Session, parsed_data: Dict[str, Any]) -> JobDescription:
    """
    Save parsed job description data to the database.

    Args:
        db (Session): SQLAlchemy session.
        parsed_data (Dict[str, Any]): Parsed job description fields.

    Returns:
        JobDescription: The saved job description instance.
    """
    job = JobDescription(**parsed_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_description_by_id(db: Session, job_id: int) -> JobDescription:
    return db.query(JobDescription).filter(JobDescription.id == job_id).first()


def list_job_descriptions(db: Session) -> List[JobDescription]:
    return db.query(JobDescription).order_by(JobDescription.created_at.desc()).all()
