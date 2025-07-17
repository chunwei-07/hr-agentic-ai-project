from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateScore(BaseModel):
    """Data model for a single candidate's score and justification."""
    candidate_id: str = Field(description="The unique identifier for the candidate.")
    score: int = Field(description="The match score for the candidate, from 1 (poor match) to 10 (perfect match).")
    justification: str = Field(description="A brief, 1-2 sentence justification for the assigned score.")
    full_resume_text: Optional[str] = Field(None, description="The full, original text of the candidate's resume for further analysis.")

class ScreeningReport(BaseModel):
    """Data model for the final screening report."""
    job_title: str = Field(description="The title of the job being screened for.")
    ranked_candidates: List[CandidateScore] = Field(description="An ordered list of candidates, ranked from highest to lowest score.")