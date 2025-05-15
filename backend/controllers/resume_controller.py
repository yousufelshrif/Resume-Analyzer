from typing import List, Optional
from sqlalchemy.orm import Session
from models.resume_model import Resume
from services.resume_service import (
    extract_resume_data,
    save_resume,
    get_resume_by_id,
    list_resumes
)


def create_resume_from_file(db: Session, file_path: str) -> Resume:
    """
    Controller that extracts structured data from a resume file
    and saves it to the database.

    Args:
        db (Session): SQLAlchemy DB session.
        file_path (str): Path to the uploaded resume file.

    Returns:
        Resume: Persisted resume instance.
    """
    parsed_data = extract_resume_data(file_path)
    return save_resume(db, parsed_data)


def fetch_resume_by_id(db: Session, resume_id: int) -> Optional[Resume]:
    """
    Controller to fetch a single resume by ID.

    Args:
        db (Session): DB session.
        resume_id (int): Resume ID.

    Returns:
        Resume or None
    """
    return get_resume_by_id(db, resume_id)


def fetch_all_resumes(db: Session) -> List[Resume]:
    """
    Controller to retrieve all resumes, sorted by creation time.

    Args:
        db (Session): SQLAlchemy DB session.

    Returns:
        List[Resume]: All resumes in the system.
    """
    return list_resumes(db)
