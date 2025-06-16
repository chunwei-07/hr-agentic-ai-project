from pydantic import BaseModel, Field
from typing import List

class CandidateDetails(BaseModel):
    """Structured data model for a candidate's resume."""
    candidate_id: str = Field(description="A unique identifier for the candidate.")
    extracted_skills: List[str] = Field(description="A list of skills extracted from the resume.")
    experience_years: int = Field(description="The total years of professional experience.")
    pii_masked: bool = Field(description="A flag indicating if Personally Identifiable Information has been masked.", default=False)