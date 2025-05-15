from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os

from database.connection import get_db
from controllers.resume_controller import (
    create_resume_from_file,
    fetch_resume_by_id,
    fetch_all_resumes
)
from schemas.resume_schema import ResumeRead

import tempfile
import shutil

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeRead, status_code=status.HTTP_201_CREATED)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and extract data from a resume file (PDF or DOCX).
    """
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are supported.")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    try:
        return create_resume_from_file(db, temp_file_path)
    finally:
        # Clean up temp file
        try:
            os.remove(temp_file_path)
        except Exception:
            pass


@router.get("/", response_model=List[ResumeRead])
def get_all_resumes(db: Session = Depends(get_db)):
    """
    Fetch all resumes stored in the database.
    """
    return fetch_all_resumes(db)


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume_by_id(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific resume by its ID.
    """
    resume = fetch_resume_by_id(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return resume
