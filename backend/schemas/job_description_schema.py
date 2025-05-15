from pydantic import BaseModel
from typing import Optional

class JobDescriptionBase(BaseModel):
    raw_text: str

class JobDescriptionCreate(JobDescriptionBase):
    required_skills: Optional[str] = None
    required_education: Optional[str] = None
    required_experience: Optional[str] = None
    required_certifications: Optional[str] = None
    required_languages: Optional[str] = None

class JobDescriptionRead(JobDescriptionCreate):
    id: int

    model_config = {
        "from_attributes": True  # Enables ORM-to-Pydantic conversion (replacement for orm_mode=True)
    }
