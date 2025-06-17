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
    You are an expert HR recruiting manager. Your task is to analyze a job description and a list of candidates, then rank them based on suitability.

    **Job Description Details:**
    Title: {job_title}
    Required Experience: {required_experience} years
    Required Skills: {required_skills}

    **Candidate Profiles:**
    {candidate_profiles}

    **Instructions:**
    1. Carefully review each candidate's profile against the job requirements.
    2. Assign a suitability score from 1 to 10, where 10 is a perfect match. Consider both skills overlap and years of experience. A candidate with all required skills and equal or greater experience should score highly.
    3. Provide a concise, 1-2 sentence justification for your score, highlighting key strengths or weaknesses.
    4. Return a ranked list of all candidates from best to worst match.

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
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