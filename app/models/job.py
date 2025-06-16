from pydantic import BaseModel, Field
from typing import List

class JobDetails(BaseModel):
    """Structured data model for a job description."""
    job_title: str = Field(description="The official title of the job position.")
    required_skills: List[str] = Field(description="A list of essential technical or soft skills.")
    required_experience_years: int = Field(description="The minimum number of years of experience required.")
    key_responsibilities: List[str] = Field(description="A list of key responsibilities for the role.")