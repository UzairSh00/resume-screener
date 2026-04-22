from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScreeningResponse(BaseModel):
    id: int
    candidate_name: str
    job_title: str
    match_score: str
    missing_skills: str
    suggestions: str
    created_at: datetime

    class Config:
        from_attributes = True

class ScreeningResult(BaseModel):
    match_score: str
    missing_skills: str
    suggestions: str