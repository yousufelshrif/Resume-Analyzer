from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from controllers.match_controller import (
    create_match_result,
    get_match_result_by_ids,
    get_all_match_results
)
from schemas.match_result_schema import MatchResultRead, MatchResultBase

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/", response_model=MatchResultRead, status_code=status.HTTP_201_CREATED)
def match_resume_to_job(
    payload: MatchResultBase,
    db: Session = Depends(get_db)
):
    """
    Create and store a new match result between a resume and a job description.
    """
    match = create_match_result(
        db=db,
        resume_id=payload.resume_id,
        job_id=payload.job_description_id,
        result_data=payload.model_dump()
    )
    return match


@router.get("/", response_model=List[MatchResultRead])
def get_all_matches(db: Session = Depends(get_db)):
    """
    Retrieve all match results stored in the system.
    """
    return get_all_match_results(db)


@router.get("/{resume_id}/{job_id}", response_model=MatchResultRead)
def get_match_by_ids(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific match result using resume ID and job ID.
    """
    match = get_match_result_by_ids(db, resume_id, job_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match result not found.")
    return match
