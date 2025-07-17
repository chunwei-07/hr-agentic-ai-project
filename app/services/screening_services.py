from sqlmodel import Session, select
from app.core.database import engine
from app.models.job import Job, JobDetails
from app.models.candidate import Candidate, CandidateDetails

# Import all agents
from app.agents.job_parser import job_parser_agent
from app.agents.resume_screener import resume_screener_agent
from app.agents.candidate_matcher import candidate_matcher_agent


# # --- MOCK DATA ---
# JOB_DESCRIPTION = """
# Position: Senior Python Developer
# Location: Remote
# Experience: 5+ years

# Responsibilities:
# - Design and develop scalable backend services.
# - Work with databases like PostgreSQL and Redis.
# - Create and maintain CI/CD pipelines.
# - Mentor junior developers.

# Required Skills:
# - Expert in Python and FastAPI.
# - Strong knowledge of SQL and database design.
# - Experience with Docker and Kubernetes.
# """

# RESUME_1 = """
# John Doe | Senior Software Engineer
# Email: john.doe@email.com | Phone: 123-456-7890

# Summary:
# A seasoned engineer with 8 years of experience in backend development, 
# specializing in Python, Django, and FastAPI. Proficient with Docker, 
# cloud services (AWS), and PostgreSQL.
# """

# RESUME_2 = """
# Jane Smith | Software Developer
# Email: jane.s@email.com

# Recent graduate with a passion for Python development. 
# Completed a project using Flask and SQL. Eager to learn
# about cloud technologies and scalable systems. 2 years of internship experience.
# """


# def run_screening_pipeline():
#     """
#     The main orchestration function that runs the entire screening process.
#     """
#     print("Starting HR Recruitment Process...")

#     # Step 1: Parse the job desc using intelligent agent
#     structured_job = job_parser_agent(JOB_DESCRIPTION)
#     print("\n--- JOB DETAILS PARSED ---")
#     print(structured_job.model_dump_json(indent=2))   # pretty print pydantic object to json

#     # Step 2: Screen all candidate resumes
#     resumes_to_process = [RESUME_1, RESUME_2]
#     all_candidate_profiles = []
#     print("\n--- SCREENING CANDIDATES ---")
#     for i, resume in enumerate(resumes_to_process):
#         print(f"\nProcessing Candidate #{i+1}...")
#         candidate_profile = resume_screener_agent(resume)
#         all_candidate_profiles.append(candidate_profile)
#         print("\n--- CANDIDATE PROFILE ---")
#         print(candidate_profile.model_dump_json(indent=2))

#     # TODO: candidate_matcher_agent

#     print("\nPipeline finished (for now).")

def run_screening_pipeline_for_job(job_id: int):
    """
    Runs the full screening pipeline for a specific job ID from the database.
    """
    print(f"\n{'='*20} STARTING PIPELINE FOR JOB ID: {job_id} {'='*20}")

    with Session(engine) as session:
        # --- Step 1: Fetch Job and its Applicants from DB ---
        job = session.get(Job, job_id)
        if not job:
            print(f"Error: Job with ID {job_id} not found.")
            return
        
        applicants = job.candidates
        if not applicants:
            print(f"No applicants found for job '{job.title}'.")
            return
        
        print(f"Found job: '{job.title}' with {len(applicants)} applicant(s).")

        # --- Step 2: Parse Job Description ---
        # In a real app, the job description would be stored in the DB.
        mock_job_description_text = f"Title: {job.title}. Required Experience: {job.experience_years_required} years."
        # Can add more details here if needed
        parsed_job_details = job_parser_agent(mock_job_description_text)
        # Can override the LLM's parsed title with the one from our DB for consistency
        parsed_job_details.job_title = job.title


        # --- Step 3: Screen each Applicant's Profile ---
        all_candidate_profiles = []
        print("\n--- Screening all applicants... ---")
        for applicant in applicants:
            # In a real app, full resume text would be stored in DB.
            mock_resume_text = f"Name: {applicant.name}. Experience: {applicant.experience_years} years. Skills: {applicant.skills_string}"

            # The resume_screener_agent already handles PII masking and parsing
            # For this DB-driven flow, we can create the CandidateDetails directly
            # to save on LLM calls, but we'll run the agent to test the full flow.

            # Using the agent to simulate the full flow
            profile = resume_screener_agent(mock_resume_text)
            profile.candidate_id = f"CAND_{applicant.id}"  # Use DB ID for consistency

            all_candidate_profiles.append(profile)
            print(f"Processed profile for {applicant.name} (ID: {profile.candidate_id})")

        
        # --- Step 4: Run the Matching Agent to get the final report ---
        print("\n--- Generating final screening report... ---")
        final_report = candidate_matcher_agent(parsed_job_details, all_candidate_profiles)

        # --- Step 5: Print the final report ---
        print(f"\n{'='*20} FINAL REPORT FOR '{job.title}' {'='*20}")
        print(final_report.model_dump_json(indent=2))
        return final_report


if __name__ == "__main__":
    run_screening_pipeline_for_job(job_id=1)  # Test for Senior Python Developer