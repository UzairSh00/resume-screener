from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Screening(Base):
    __tablename__ = "screenings"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(100))
    job_title = Column(String(200))
    job_description = Column(Text)
    resume_text = Column(Text)
    match_score = Column(String(10))
    missing_skills = Column(Text)
    suggestions = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())