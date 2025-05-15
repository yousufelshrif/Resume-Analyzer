from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, DateTime
from datetime import datetime
from base import Base  # Assumes you're using the same DeclarativeBase as Resume

class JobDescription(Base):
    """
    SQLAlchemy model for storing parsed job descriptions.

    This table stores both the raw job description text and all structured fields 
    extracted from it (e.g., required skills, experience, education). It's designed 
    for comparison with parsed resumes in talent matching systems.

    Attributes:
        id (int): Primary key identifier.
        title (str): Job title (e.g., Backend Engineer, Data Scientist).
        company (str): Name of the company posting the job.
        raw_text (str): Unstructured raw text from the job description.
        required_skills (str | None): JSON stringified list of required skills.
        required_experience (str | None): JSON stringified list of experience phrases or years.
        required_certifications (str | None): JSON stringified list of required certifications.
        required_languages (str | None): JSON stringified list of required spoken/written languages.
        required_education (str | None): JSON stringified degree/field requirements.
        created_at (datetime): Timestamp of when this job description was stored.
    """

    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    company: Mapped[str] = mapped_column(String, nullable=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)

    required_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_certifications: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_languages: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_education: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
