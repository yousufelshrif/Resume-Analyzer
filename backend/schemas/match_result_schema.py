from pydantic import BaseModel

class MatchResultBase(BaseModel):
    resume_id: int
    job_description_id: int
    match_score: float

class MatchResultRead(MatchResultBase):
    id: int

    model_config = {
        "from_attributes": True  
    }
