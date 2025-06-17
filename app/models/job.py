from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

# Forward reference for the linking model
class JobApplication(SQLModel, table=True):
    job_id: Optional[int] = Field(default=None, foreign_key="job.id", primary_key=True)
    candidate_id: Optional[int] = Field(default=None, foreign_key="candidate.id", primary_key=True)
    status: str = Field(default="Applied")

class Job(SQLModel, table=True):
    """Database model for a job description."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    experience_years_required: int

    # This defines the M2M relationship
    # Links a Job to many Candidates through the JobApplication table
    candidates: List["Candidate"] = Relationship(back_populates="jobs", link_model=JobApplication)

class JobDetails(SQLModel):
    """Pydantic-like model for structured data from LLM (not a DB table)."""
    job_title: str
    required_skills: List[str]
    required_experience_years: int
    key_responsibilities: List[str]