import os
from dotenv import load_dotenv
from app.services.screening_services import run_screening_pipeline_for_job
from scripts.seed_db import seed_database

def main():
    # Load environment variables
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")

    # Ensure the database is seeded
    print("--- Ensuring database is seeded ---")
    seed_database()

    # --- Run the full, end-to-end pipeline ---
    run_screening_pipeline_for_job(job_id=1)

if __name__ == "__main__":
    main()