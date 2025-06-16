import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. SETUP ---
# Load .env
load_dotenv()

# Check if the API key is set
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# --- 2. MOCK DATA ---
JOB_DESCRIPTION = """
Position: Senior Python Developer
Location: Remote
Experience: 5+ years

Responsibilities:
- Design and develop scalable backend services.
- Work with databases like PostgreSQL and Redis.
- Create and maintain CI/CD pipelines.
- Mentor junior developers.

Required Skills:
- Expert in Python and FastAPI.
- Strong knowledge of SQL and database design.
- Experience with Docker and Kubernetes.
"""

RESUME_1 = """
John Doe | Senior Software Engineer
Email: john.doe@email.com | Phone: 123-456-7890

Summary:
A seasoned engineer with 8 years of experience in backend development,
specializing in Python, Django, and FastAPI. Profecient with Docker,
cloud services (AWS), and PostgreSQL.
"""

RESUME_2 = """
Jane Smith | Software Developer
Email: jane.s@email.com

Recent graduate with a passion for Python development.
Completed a project using Flask and SQL. Eager to learn
about cloud technologies and scalable systems. 2 years of internship experience.
"""

# --- 3. AGENT DEFINITION (Placeholder for now) ---
def job_parser_agent(job_description_text):
    """
    Takes raw job description text and returns a structured dictionary.
    """
    print("--- Calling Job Parser Agent ---")
    # TODO: Use LLM with a structured output prompt to parse this.
    print("Parsing job description...")
    # For now, return a placeholder.
    parsed_job = {
        "required_skills": ["Python", "FastAPI", "SQL", "Docker"],
        "required_experience_years": 5
    }
    print("Job parsing complete.")
    return parsed_job

def resume_screener_agent(resume_text):
    """
    Takes raw resume text, masks PII, and returns a structured dictionary.
    """
    print(f"--- Calling Resume Screener Agent for a candidate ---")
    # TODO: Implement PII masking
    # TODO: Use LLM to extract skills and experience
    print("Screening resume...")
    # Placeholder logic
    if "John Doe" in resume_text:
        parsed_resume = { "candidate_id": "CAND_001", "extracted_skills": ["Python", "FastAPI", "Docker", "PostgreSQL"], "experience_years": 8, "pii_masked": True }
    else:
        parsed_resume = { "candidate_id": "CAND_002", "extracted_skills": ["Python", "SQL"], "experience_years": 2, "pii_masked": True }
    print("Resume screening complete.")
    return parsed_resume

def candidate_matcher_agent(job_details, candidate_profiles):
    """
    Compares the job to candidates and returns a ranked list with justifications.
    """
    print("--- Calling Candidate Matcher Agent ---")
    # TODO: Implement scoring logic and use LLM for justification.
    print("Matching candidates to job...")

    final_report = f"""
    Candidate Screening Report
    ==========================
    Job Requirements: {job_details['required_experience_years']} years, Skills: {', '.join(job_details['required_skills'])}

    Top Candidates:
    1. Candidate ID: {candidate_profiles[0]['candidate_id']} - Score: 9/10. Stromg match on all skills and experience.
    2. Candidate ID: {candidate_profiles[1]['candidate_id']} - Score: 6/10. Matches key skills but lacks required experience and containerization knowledge.
    """
    print("Matching complete.")
    return final_report


# --- 4. ORCHESTRATION ---
if __name__ == "__main__":
    print("Starting HR Recruitment Process...")

    # Step 1: Parse the job description
    structured_job = job_parser_agent(JOB_DESCRIPTION)

    # Step 2: Screen all candidate resumes
    resumes = [RESUME_1, RESUME_2]
    structured_resumes = []
    for resume in resumes:
        structured_resumes.append(resume_screener_agent(resume))

    # Step 3: Match the candidates to the job and generate a report
    report = candidate_matcher_agent(structured_job, structured_resumes)

    # Final Output
    print("\n--- FINAL REPORT ---")
    print(report)