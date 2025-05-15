from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Float, String, Text, DateTime
from datetime import datetime
from base import Base  # Import your DeclarativeBase

class ResumeMatchResult(Base):
    """
    SQLAlchemy model for storing resume-to-job matching results.

    This table represents the comparison output between a parsed resume
    and a job description. It can be used in ATS systems, recommendation engines,
    and recruiter dashboards to rank candidates.

    Attributes:
        id (int): Primary key identifier.
        resume_id (int): Foreign key to the Resume being matched.
        job_description_id (int): Foreign key to the matched JobDescription.
        match_score (float): Final matching score (e.g., 0.0 to 100.0).
        matched_skills (str | None): JSON stringified list of overlapping skills.
        missing_skills (str | None): JSON stringified list of missing skills.
        notes (str | None): Optional explanation or justification for match score.
        created_at (datetime): Timestamp of when this match result was generated.
    """

    __tablename__ = "resume_match_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False)
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id"), nullable=False)

    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_skills: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    missing_skills: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
