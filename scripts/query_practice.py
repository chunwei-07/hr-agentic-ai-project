from sqlmodel import Session, select
from app.core.database import engine
from app.models.job import Job
from app.models.candidate import Candidate

def practice_queries():
    print("--- Practicing SQL Queries with SQLModel ---")
    with Session(engine) as session:

        # Query 1: Find all candidates for the "Senior Python Developer" job
        print("\n[Query 1: Find all applicants for Senior Python Developer]")
        statement = select(Candidate).join(Job.candidates).where(Job.title == "Senior Python Developer")
        results = session.exec(statement).all()
        for candidate in results:
            print(f"- {candidate.name}")

        # Query 2: Find all jobs a specific candidate applied for (Jane Smith)
        print("\n[Query 2: Find all jobs Jane Smith applied for]")
        statement = select(Job).join(Candidate.jobs).where(Candidate.name == "Jane Smith")
        results = session.exec(statement).all()
        for job in results:
            print(f"- {job.title}")
            
        # Query 3: Find all experienced candidates with Python skills
        print("\n[Query 3: Find experienced candidates (>4 years) with Python skills]")
        statement = select(Candidate).where(Candidate.experience_years > 4).where(Candidate.skills_string.like("%Python%"))
        results = session.exec(statement).all()
        for candidate in results:
            print(f"- {candidate.name} ({candidate.experience_years} years exp)")

if __name__ == "__main__":
    practice_queries()