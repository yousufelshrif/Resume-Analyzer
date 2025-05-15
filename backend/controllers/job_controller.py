from typing import List, Optional
from sqlalchemy.orm import Session
from models.job_description_model import JobDescription
from services.job_service import (
    extract_job_description,
    save_job_description,
    get_job_description_by_id,
    list_job_descriptions
)


def create_job_description(db: Session, raw_text: str) -> JobDescription:
    """
    Controller to parse and save a job description into the database.

    Args:
        db (Session): SQLAlchemy DB session.
        raw_text (str): Job description text input.

    Returns:
        JobDescription: The persisted job description.
    """
    parsed = extract_job_description(raw_text)
    return save_job_description(db, parsed)


def fetch_job_description_by_id(db: Session, job_id: int) -> Optional[JobDescription]:
    """
    Controller to retrieve a job description by its ID.

    Args:
        db (Session): SQLAlchemy DB session.
        job_id (int): Unique identifier for the job description.

    Returns:
        JobDescription or None
    """
    return get_job_description_by_id(db, job_id)


def fetch_all_job_descriptions(db: Session) -> List[JobDescription]:
    """
    Controller to fetch all job descriptions, sorted by recency.

    Args:
        db (Session): SQLAlchemy DB session.

    Returns:
        List[JobDescription]: List of all saved job descriptions.
    """
    return list_job_descriptions(db)
