from sqlmodel import SQLModel, Session
from app.core.database import engine
from app.models.job import Job
from app.models.candidate import Candidate, JobApplication

# --- MOCK DATA ---
RESUME_1_TEXT = """
John Doe | Senior Software Engineer
Email: john.doe@email.com | Phone: 123-456-7890
Summary: A seasoned engineer with 8 years of experience in backend development, 
specializing in Python, Django, and FastAPI. Proficient with Docker, 
cloud services (AWS), and PostgreSQL. Successfully led a project to migrate a monolithic
Django application to a microservices architecture using FastAPI, resulting in a 40% performance increase.
"""
RESUME_2_TEXT = """
Jane Smith | Software Developer
Email: jane.s@email.com
Recent graduate with a passion for Python development. 
Completed a capstone project building a restaurant recommendation system using Flask and SQL.
The project involved creating a public-facing API and a simple front-end. Eager to learn
about cloud technologies and scalable systems. 2 years of internship experience.
"""
RESUME_3_TEXT = """
Peter Jones | Python Developer
Email: p.jones@email.com
A detail-oriented developer with 6 years of experience. My primary expertise is in building robust
data processing pipelines with Python and Django. I have extensive experience with AWS S3 and EC2.
While I haven't used FastAPI professionally, I am a quick learner.
"""
RESUME_4_TEXT = """
Sam Ray | Senior Project Manager
Email: sam.r@email.com
An expert project manager with 10 years of experience. My primary expertise is leading a team
of 10 people to build a commercial level system that allows my previous company to earn 50% more
revenue. A rapid learner who is eager to always learn and improve.
"""

def seed_database():
    print("--- Seeding Database ---")

    # Create the tables in the database based on the models
    SQLModel.metadata.create_all(engine)

    # Use a session to interact with the database
    with Session(engine) as session:
        # Clear existing data to make the script re-runnable
        session.query(JobApplication).delete()
        session.query(Candidate).delete()
        session.query(Job).delete()

        # --- Create Job objects ---
        job1 = Job(title="Senior Python Developer", experience_years_required=5)
        job2 = Job(title="Junior Data Analyst", experience_years_required=1)

        # --- Create Candidate objects ---
        cand1 = Candidate(name="John Doe", experience_years=8, skills_string="Python,FastAPI,Docker,PostgreSQL,AWS", resume_text=RESUME_1_TEXT)
        cand2 = Candidate(name="Jane Smith", experience_years=2, skills_string="Python,SQL,Flask,Tableau", resume_text=RESUME_2_TEXT)
        cand3 = Candidate(name="Peter Jones", experience_years=6, skills_string="Python,Django,React,AWS", resume_text=RESUME_3_TEXT)
        cand4 = Candidate(name="Sam Ray", experience_years=10, skills_string="Project Management,Leadership", resume_text=RESUME_4_TEXT)

        session.add_all([job1, job2, cand1, cand2, cand3, cand4])
        session.commit()  # Commit first to assign IDs

        # --- Create the relationships (Job Applications) ---
        # John Doe applies for the Senior Python Developer job
        app1 = JobApplication(job_id=job1.id, candidate_id=cand1.id, status="Screening")
        
        # Jane Smith applies for both jobs
        app2 = JobApplication(job_id=job1.id, candidate_id=cand2.id, status="Applied")
        app3 = JobApplication(job_id=job2.id, candidate_id=cand2.id, status="Interviewing")
        
        # Peter Jones applies for the Senior Python Developer job
        app4 = JobApplication(job_id=job1.id, candidate_id=cand3.id, status="Rejected")

        # Sam Ray applies for Senior Python Developer job
        app5 = JobApplication(job_id=job1.id, candidate_id=cand4.id, status="Applied")

        # Now add JobApplications with IDs set
        session.add_all([app1, app2, app3, app4, app5])
        session.commit()

    print("--- Database seeding complete! ---")

if __name__ == "__main__":
    seed_database()