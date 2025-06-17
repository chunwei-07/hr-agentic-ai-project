from sqlmodel import SQLModel, Session
from app.core.database import engine
from app.models.job import Job
from app.models.candidate import Candidate, JobApplication

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
        cand1 = Candidate(name="John Doe", experience_years=8, skills_string="Python,FastAPI,Docker,PostgreSQL,AWS")
        cand2 = Candidate(name="Jane Smith", experience_years=2, skills_string="Python,SQL,Flask,Tableau")
        cand3 = Candidate(name="Peter Jones", experience_years=6, skills_string="Python,Django,React,AWS")

        session.add_all([job1, job2, cand1, cand2, cand3])
        session.commit()  # Commit first to assign IDs

        # --- Create the relationships (Job Applications) ---
        # John Doe applies for the Senior Python Developer job
        app1 = JobApplication(job_id=job1.id, candidate_id=cand1.id, status="Screening")
        
        # Jane Smith applies for both jobs
        app2 = JobApplication(job_id=job1.id, candidate_id=cand2.id, status="Applied")
        app3 = JobApplication(job_id=job2.id, candidate_id=cand2.id, status="Interviewing")
        
        # Peter Jones applies for the Senior Python Developer job
        app4 = JobApplication(job_id=job1.id, candidate_id=cand3.id, status="Rejected")

        # Now add JobApplications with IDs set
        session.add_all([app1, app2, app3, app4])
        session.commit()

    print("--- Database seeding complete! ---")

if __name__ == "__main__":
    seed_database()