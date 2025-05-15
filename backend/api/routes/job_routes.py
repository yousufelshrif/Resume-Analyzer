from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from controllers.job_controller import (
    create_job_description,
    fetch_job_description_by_id,
    fetch_all_job_descriptions
)
from schemas.job_description_schema import JobDescriptionCreate, JobDescriptionRead
from database.connection import get_db  #

router = APIRouter(prefix="/jobs", tags=["Job Descriptions"])


@router.post("/", response_model=JobDescriptionRead, status_code=status.HTTP_201_CREATED)
def upload_job_description(payload: JobDescriptionCreate, db: Session = Depends(get_db)):
    """
    Upload and parse a job description. Saves structured data to the database.
    """
    job = create_job_description(db, payload.raw_text)
    return job


@router.get("/{job_id}", response_model=JobDescriptionRead)
def get_job_description(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a job description by its ID.
    """
    job = fetch_job_description_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found.")
    return job


@router.get("/", response_model=List[JobDescriptionRead])
def list_job_descriptions(db: Session = Depends(get_db)):
    """
    List all saved job descriptions in descending order of creation.
    """
    return fetch_all_job_descriptions(db)
