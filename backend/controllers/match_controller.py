from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.resume_match_model import ResumeMatchResult
from services.match_result_service import (
    save_match_result,
    get_match_result,
    list_all_matches
)


def create_match_result(
    db: Session,
    resume_id: int,
    job_id: int,
    result_data: Dict[str, Any]
) -> ResumeMatchResult:
    """
    Controller to create and persist a match result between a resume and a job.

    Args:
        db (Session): Active SQLAlchemy DB session.
        resume_id (int): ID of the matched resume.
        job_id (int): ID of the matched job.
        result_data (Dict[str, Any]): Result dict containing match_score, matched/missing skills, etc.

    Returns:
        ResumeMatchResult: The newly stored match result object.
    """
    return save_match_result(db, resume_id, job_id, result_data)


def get_match_result_by_ids(db: Session, resume_id: int, job_id: int) -> ResumeMatchResult | None:
    """
    Controller to retrieve a specific match result.

    Args:
        db (Session): DB session.
        resume_id (int): Resume ID.
        job_id (int): Job Description ID.

    Returns:
        ResumeMatchResult or None
    """
    return get_match_result(db, resume_id, job_id)


def get_all_match_results(db: Session) -> List[ResumeMatchResult]:
    """
    Controller to list all stored match results sorted by recency.

    Args:
        db (Session): SQLAlchemy DB session.

    Returns:
        List[ResumeMatchResult]: List of all match results.
    """
    return list_all_matches(db)
