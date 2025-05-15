from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text,DateTime
from base import Base
from datetime import datetime

class Resume(Base):
    """
    SQLAlchemy model for storing parsed resume data.

    This table stores both the raw text and structured information extracted from
    resumes. It is used in systems like resume parsers, job matchers, and ATS platforms.

    Attributes:
        id (int): Auto-incremented primary key.
        file_name (str): Name of the uploaded resume file.
        raw_text (str): Full plain-text extracted from the resume.
        parsed_email (str | None): Extracted primary email address.
        parsed_phone (str | None): Extracted phone number.
        parsed_links (str | None): JSON stringified list of external links (LinkedIn, GitHub, etc.).
        parsed_skills (str | None): JSON stringified list of detected skills.
        parsed_experience (str | None): JSON stringified structured experience block.
        parsed_education (str | None): JSON stringified structured education block.
        parsed_certifications (str | None): JSON stringified list of certifications.
        parsed_languages (str | None): JSON stringified list of languages.
        parsed_projects (str | None): JSON stringified list of projects.
        parsed_interests (str | None): JSON stringified list of hobbies/interests.
        created_at (datetime): Timestamp when the resume was parsed/stored.
    """

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)

    parsed_email: Mapped[str | None] = mapped_column(String, nullable=True)
    parsed_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    parsed_links: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_education: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_certifications: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_languages: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_projects: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_interests: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
