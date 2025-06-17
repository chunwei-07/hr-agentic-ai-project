from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List

from app.models.job import JobDetails
from app.models.candidate import CandidateDetails
from app.models.report import ScreeningReport

import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key=google_api_key,
                             temperature=0.1)

# We will add a "few-shot" example to improve the output quality.
FEW_SHOT_EXAMPLE = """
Example Input:
Job Title: UI/UX Designer
Required Experience: 3 years
Required Skills: Figma, User Research, Prototyping

Candidate Profiles:
Candidate ID: CAND_EX1
Experience: 5 years
Skills: Figma, Prototyping, Adobe XD, User Interviews

Candidate ID: CAND_EX2
Experience: 2 years
Skills: Figma, HTML, CSS

Example Output:
{
  "job_title": "UI/UX Designer",
  "ranked_candidates": [
    {
      "candidate_id": "CAND_EX1",
      "score": 9,
      "justification": "Strong candidate. Exceeds experience requirement and possesses all key skills, including the crucial 'User Research' (as User Interviews)."
    },
    {
      "candidate_id": "CAND_EX2",
      "score": 5,
      "justification": "Weak match. Lacks the required experience and the critical 'User Research' skill."
    }
  ]
}
"""

def candidate_matcher_agent(job_details: JobDetails, candidate_profiles: List[CandidateDetails]) -> ScreeningReport:
    """
    Compares the job to candidates and returns a ranked list with justifications.
    """
    print("--- Calling Candidate Matcher Agent ---")

    # Format the candidate profiles into a single string for the prompt
    candidate_profiles_str = "\n\n".join(
        [f"Candidate ID: {c.candidate_id}\nExperience: {c.experience_years} years\nSkills: {', '.join(c.extracted_skills)}"
         for c in candidate_profiles]
    )

    parser = PydanticOutputParser(pydantic_object=ScreeningReport)

    prompt_template = """
    You are a meticulous and unbiased expert HR recruitment manager. Your primary goal is to provide a quantitative and
    qualitative assessment of candidates based strictly on the information provided.

    **Role and Goal:**
    Analyze the provided job description and candidate profiles. Rank the candidates based on their suitability for the role.

    **Constraints:**
    - Base your assessment ONLY on the information given. Do not infer skills or experience that are not explicitly mentioned.
    - The score must be an integer between 1 and 10.
    - Justifications must be brief (1-2 sentences) and directly reference the job requirements.
    - Adhere strictly to the JSON output format provided.

    **Here is an example of the expected input and output format:**
    {few_shot_example}

    **Now, perform the analysis for the following real request:**

    **Job Description Details:**
    Title: {job_title}
    Required Experience: {required_experience} years
    Required Skills: {required_skills}

    **Candidate Profiles to Analyze:**
    {candidate_profiles}

    **Output JSON:**
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "few_shot_example": FEW_SHOT_EXAMPLE
        }
    )

    chain = prompt | llm | parser

    print("Matching candidates to job with LLM...")

    report = chain.invoke({
        "job_title": job_details.job_title,
        "required_experience": job_details.required_experience_years,
        "required_skills": ", ".join(job_details.required_skills),
        "candidate_profiles": candidate_profiles_str
    })

    print("Matching complete.")
    return report