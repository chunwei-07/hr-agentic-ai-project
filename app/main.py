from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from app.core.caching import setup_langchain_cache
from app.services.screening_services import run_screening_pipeline_for_job
from app.services.rag_service import create_rag_chain, load_and_build_vector_store, create_text_rag_chain
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
    
    load_and_build_vector_store()
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

# --- Pydantic Models ---
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

class DrillDownRequest(BaseModel):
    context_text: str
    question: str


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
    

@app.post("/ask_rag", response_model=AnswerResponse)
def ask_rag_question(request: QuestionRequest):
    """
    Asks a question to the RAG system about the indexed candidate resumes.
    """
    try:
        print(f"--- Received RAG question: {request.question} ---")
        rag_chain = create_rag_chain()
        response = rag_chain.invoke({"input": request.question})
        return AnswerResponse(answer=response['answer'])
    except Exception as e:
        print(f"An error occurred in RAG chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/ask_drill_down", response_model=AnswerResponse)
def ask_drill_down_question(request: DrillDownRequest):
    """
    Performs a RAG query on a specific provided text (e.g., a single resume).
    This allows for a "drill-down" analysis.
    """
    try:
        print(f"--- Received drill-down question: {request.question} ---")
        text_rag_chain = create_text_rag_chain(request.context_text)
        response = text_rag_chain.invoke({"input": request.question})
        return AnswerResponse(answer=response['answer'])
    except Exception as e:
        print(f"An error occurred in drill-down chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))