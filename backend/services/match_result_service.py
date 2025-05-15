from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models.resume_match_model import ResumeMatchResult
import json


def save_match_result(db: Session, resume_id: int, job_id: int, result: Dict[str, Any]) -> ResumeMatchResult:
    """
    Save the resume-to-job match result into the database.

    Args:
        db (Session): SQLAlchemy session.
        resume_id (int): ID of the matched resume.
        job_id (int): ID of the matched job.
        result (Dict[str, Any]): Match result containing score, matched/missing fields.

    Returns:
        ResumeMatchResult: The saved match result instance.
    """
    match = ResumeMatchResult(
        resume_id=resume_id,
        job_id=job_id,
        match_score=result.get("match_score"),
        matched_skills=json.dumps(result.get("matched_skills"), ensure_ascii=False),
        missing_skills=json.dumps(result.get("missing_skills"), ensure_ascii=False),
        notes=result.get("notes")
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_match_result(db: Session, resume_id: int, job_id: int) -> ResumeMatchResult:
    """
    Retrieve a specific resume-to-job match result from the database.

    Args:
        db (Session): SQLAlchemy session.
        resume_id (int): Resume ID.
        job_id (int): Job ID.

    Returns:
        ResumeMatchResult: The match result if found, otherwise None.
    """
    return db.query(ResumeMatchResult).filter(
        ResumeMatchResult.resume_id == resume_id,
        ResumeMatchResult.job_id == job_id
    ).first()


def list_all_matches(db: Session) -> List[ResumeMatchResult]:
    """
    List all resume-job match results in the system.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[ResumeMatchResult]: All stored match results.
    """
    return db.query(ResumeMatchResult).order_by(ResumeMatchResult.created_at.desc()).all()
