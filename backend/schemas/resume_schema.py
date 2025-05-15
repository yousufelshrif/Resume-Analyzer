from pydantic import BaseModel
from typing import Optional

class ResumeBase(BaseModel):
    file_name: str
    raw_text: str

class ResumeCreate(ResumeBase):
    parsed_email: Optional[str] = None
    parsed_phone: Optional[str] = None
    parsed_links: Optional[str] = None
    parsed_skills: Optional[str] = None
    parsed_experience: Optional[str] = None
    parsed_education: Optional[str] = None
    parsed_certifications: Optional[str] = None
    parsed_languages: Optional[str] = None
    parsed_projects: Optional[str] = None
    parsed_interests: Optional[str] = None

class ResumeRead(ResumeCreate):
    id: int

    model_config = {
        "from_attributes": True 
    }
