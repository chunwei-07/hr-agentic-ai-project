from app.agents.job_parser import job_parser_agent
from app.agents.resume_screener import resume_screener_agent
# TODO: Import other agents


# --- MOCK DATA ---
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
specializing in Python, Django, and FastAPI. Proficient with Docker, 
cloud services (AWS), and PostgreSQL.
"""

RESUME_2 = """
Jane Smith | Software Developer
Email: jane.s@email.com

Recent graduate with a passion for Python development. 
Completed a project using Flask and SQL. Eager to learn
about cloud technologies and scalable systems. 2 years of internship experience.
"""


def run_screening_pipeline():
    """
    The main orchestration function that runs the entire screening process.
    """
    print("Starting HR Recruitment Process...")

    # Step 1: Parse the job desc using intelligent agent
    structured_job = job_parser_agent(JOB_DESCRIPTION)
    print("\n--- JOB DETAILS PARSED ---")
    print(structured_job.model_dump_json(indent=2))   # pretty print pydantic object to json

    # Step 2: Screen all candidate resumes
    resumes_to_process = [RESUME_1, RESUME_2]
    all_candidate_profiles = []
    print("\n--- SCREENING CANDIDATES ---")
    for i, resume in enumerate(resumes_to_process):
        print(f"\nProcessing Candidate #{i+1}...")
        candidate_profile = resume_screener_agent(resume)
        all_candidate_profiles.append(candidate_profile)
        print("\n--- CANDIDATE PROFILE ---")
        print(candidate_profile.model_dump_json(indent=2))

    # TODO: candidate_matcher_agent

    print("\nPipeline finished (for now).")