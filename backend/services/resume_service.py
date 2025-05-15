from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models.resume_model import Resume
from ...ai.extractors.resume.resume_extractor import ResumeExtractor
from ...ai.extractors.resume.text_extractor import ResumeTextExtractor
import os
import json


def extract_resume_data(file_path: str) -> Dict[str, Any]:
    """
    Extract structured resume information from a PDF or DOCX file.

    Args:
        file_path (str): Absolute path to the uploaded resume file.

    Returns:
        Dict[str, Any]: Parsed fields suitable for storing in the Resume model.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If text extraction fails or yields insufficient content.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text_extractor = ResumeTextExtractor(file_path)
    raw_text = text_extractor.extract_text()

    if not raw_text or len(raw_text.strip()) < 20:
        raise ValueError("Text extraction failed or content is too short.")

    extractor = ResumeExtractor()
    parsed = extractor.parse(raw_text)

    def to_json(value: Any) -> str | None:
        if value is None:
            return None
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return None

    resume_data: Dict[str, Any] = {
        "file_name": os.path.basename(file_path),
        "raw_text": raw_text,
        "parsed_email": parsed.get("Email"),
        "parsed_phone": parsed.get("Phone"),
        "parsed_links": to_json(parsed.get("Links")),
        "parsed_skills": to_json(parsed.get("Skills")),
        "parsed_experience": to_json(parsed.get("Experience")),
        "parsed_education": to_json(parsed.get("Education")),
        "parsed_certifications": to_json(parsed.get("Certifications")),
        "parsed_languages": to_json(parsed.get("Languages")),
        "parsed_projects": to_json(parsed.get("Projects")),
        "parsed_interests": to_json(parsed.get("Interests")),
    }

    return resume_data


def save_resume(db: Session, parsed_data: Dict[str, Any]) -> Resume:
    """
    Save parsed resume data to the database.

    Args:
        db (Session): SQLAlchemy DB session.
        parsed_data (Dict[str, Any]): Parsed resume fields.

    Returns:
        Resume: The saved Resume instance.
    """
    resume = Resume(**parsed_data)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_resume_by_id(db: Session, resume_id: int) -> Resume:
    return db.query(Resume).filter(Resume.id == resume_id).first()


def list_resumes(db: Session) -> List[Resume]:
    return db.query(Resume).order_by(Resume.created_at.desc()).all()
