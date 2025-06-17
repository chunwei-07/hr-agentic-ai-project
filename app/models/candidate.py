from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from .job import Job, JobApplication

class Candidate(SQLModel, table=True):
    """Database model for a candidate's profile."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # Real name for DB purposes
    experience_years: int
    # In a real app, skills might be a seperate table, but a simple string is fine for now
    skills_string: str

    # Defines the relationship back to Job
    jobs: List[Job] = Relationship(back_populates="candidates", link_model=JobApplication)

class CandidateDetails(SQLModel):
    """Pydantic-like model for structured data from LLM after screening."""
    candidate_id: Optional[str] = None
    extracted_skills: List[str]
    experience_years: int
    pii_masked: Optional[bool] = None