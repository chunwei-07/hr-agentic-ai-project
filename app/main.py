from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from app.core.caching import setup_langchain_cache
from app.services.screening_services import run_screening_pipeline_for_job
from scripts.seed_db import seed_database
from app.models.report import ScreeningReport

# --- Application Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("--- Application starting up... ---")
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ:
        raise RuntimeError("GOOGLE_API_KEY not found in .env file.")
    
    setup_langchain_cache()
    seed_database()

    yield

    # Code to run on shutdown
    print("--- Application shutting down... ---")


# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic HR Screening API",
    description="An API for screening job candidates using an agentic AI system.",
    version="1.0.0",
    lifespan=lifespan
)


# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Agentic HR Screening API!"}


@app.post("/screen/{job_id}", response_model=ScreeningReport)
def screen_candidates_for_job(job_id: int):
    """
    Triggers the end-to-end screening pipeline for a given job ID.
    """
    try:
        print(f"--- Received request to screen for job_id: {job_id} ---")
        report = run_screening_pipeline_for_job(job_id)
        if report is None:
            raise HTTPException(status_code=404, detail=f"No report generated. Job ID {job_id} might not have applicants or exist.")
        return report
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))