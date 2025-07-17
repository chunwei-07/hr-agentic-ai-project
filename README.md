# Agentic HR Screening & Analysis Platform
This project is a sophisticated, dual-purpose AI platform designed to accelerate and enhance the HR recruitment process. It moves beyond a single tool, offering two distinct, powerful workflows to tackle common recruiting challenges - whether dealing with structured data in a modern HR system or unstructured documents in a simple folder.

The entire system is built as a professional, containerized web service with a clear API.

![System Architecture](architecture.png)

## System Architecture & Workflow

### Component Breakdown
- **User / Client App (Blue):** The entry point for any request. This can be a human user interacting with the API documentation or another automated system.
- **FastAPI Gateway (Blue):** The web server that receives all incoming HTTP requests. It handles API routing, data validation, and response formatting, but delegates the core business logic.
- **Screening Service (Orchestrator):** The central brain of the application. It manages the end-to-end workflow, coordinating between the database and the various AI agents.
- **Data Stores (Yellow):**
  - **SQLite Database:** The primary relational database for storing persistent, structured data like job information and candidate profiles.
  - **FAISS Vector Store:** A specialized database used to store vector embeddings of resumes for efficient similarity searched (used by the RAG Q&A functionality).
- **Agentic Core (Green):** The specialized AI workers that perform specific tasks.
  - **Job Parser, Resumer Screener, Candidate Matcher Agents:** Each agent is an LLM-powered chain responsible for a single, well-defined task.
  - **PII Masker:** A critical utility used by the `Resume Screener` to anonymize data before it is processed by the LLM, ensuring privacy and compliance.
- **Caching & External Services (Red):**
  - **Langchain Cache:** A performance-enhancing layer that intercepts all LLM calls. It stores the results of previous calls to avoid redundant, costly, and time-consuming API requests.
  - **Google Gemini API:** The external Large Language Model that provides the core reasoning and language understanding capabilities for all agents.

## 🚀 The Two Core Workflows
This platform offers two primary solutions, each designed for a different business need:

### 1. The Integrated Screening & Drill-Down Workflow
+  **Problem Solved:** For the organized company with an existing HR database (ATS/HRIS). How do you intelligently rank existing applicants and then perform deep, nuanced analysis on the top candidates?
+  **Our Solution:** A multi-step process that first uses an AI agent system to score and rank all applicants for a job from the database. The API response then includes the full resume text of top candidates, allowing an HR manager to immediately use our "Drill-Down" API to ask specific, context-aware questions about a single candidate's experience.
### 2. The Broad RAG Discovery Workflow
+  **Problem Solved:** For the HR manager who has a folder full of unstructured PDF resumes. How do you quickly find relevant candidates without reading every single document?
+  **Our Solution:** A powerful Retrieval-Augmented Generation (RAG) system that ingests an entire directory of PDFs. It allows the user to ask broad, natural language questions across the entire candidate pool (e.g., "Which candidates have experience with cloud platforms?") to discover talent quickly.


## 🌟 Key Features
+  **Dual-Workflow System:** Tackles both structured database screening and unstructured document discovery.
+  **Advanced Agentic AI:** A multi-agent system (using LangChain & Gemini-2.0-Flash) collaborates to parse, screen, and perform complex reasoning for candidate matching.
+  **Context-Aware "Drill-Down":** A unique feature that allows users to seamlessly transition from a high-level ranked list to an in-depth "chat" with a single candidate's resume.
+  **Ethical & Compliant:** Features automatic PII (Personally Identifiable Information) masking by default to ensure candidate privacy.
+  **Optimized & Scalable:** A persistent caching layer drastically reduces API latency and costs, and the entire application is containerized with Docker for easy deployment.
+  **Professional API with Interactive Docs:** Built with FastAPI, providing a high-performance backend and automatic, interactive documentation.
+  **Robust Data Foundation:** Uses SQLModel and SQLAlchemy to interact with a relational database (SQLite), making it easily adaptable to production systems like PostgreSQL.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **AI/LLM**: LangChain, Google Gemini-2.0-Flash
- **Database**: SQLModel, SQLAlchemy, SQLite
- **DevOps**: Docker, Docker Compose
- **Tooling**: Pydantic, Presidio for PII masking, FAISS (for in-memory vector search)

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- A Google Gemini API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chunwei-07/hr-agentic-ai-project.git
    cd hr-agentic-ai-project
    ```

2.  **Create the environment file:**
    Create a file named `.env` in the project root and add your API key:
    ```
    GOOGLE_API_KEY="your_secret_google_api_key_here"
    ```

3.  **Build and run the application with Docker Compose:**
    This is the recommended method as it handles everything for you.
    ```bash
    docker-compose up --build
    ```
    OR ALTERNATIVELY:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://127.0.0.1:8000`.

## Usage

The best way to interact with the API is through the auto-generated documentation.

**Navigate to `http://127.0.0.1:8000/docs` in your browser.**

### Demo 1: The Integrated Screening & Drill-Down Workflow
This demo shows how to analyze candidates from a structured database.

**Step 1: Get Ranked Candidates**
+  Go to the `POST /screen/{job_id}` endpoint.
+  Enter `1` for the `job_id` and click "Execute."
+  **Observe:** The system returns a ranked list of candidates for the "Senior Python Developer" role. Notice the top candidate's score, justification, and the included `full_resume_text`.

**Step 2: Perform Drill-Down Analysis**
+  Copy the `full_resume_text` of the top candidate (John Doe).
+  Go to the `POST /ask_drill_down` endpoint.
+  Paste the resume text into the `context_text` field.
+  In the `question` field, ask a specific question like: `"What was the specific result of the Django migration project he led?"`
+  **Observe:** The AI reads only the provided text and gives a precise answer: `"The project resulted in a 40% performance increase."`

### Demo 2: The Broad RAG Discovery Workflow
This demo shows how to find talent from a folder of unstructured PDFs.

+  Go to the `POST /ask_rag` endpoint.
+  In the `request body`, enter a question to search across all PDF resumes, such as: `"Who has experience with Flask and SQL?"`
+  **Observe:** The system provides a direct answer by searching its vector index of all the documents, identifying Jane Smith as the relevant candidate.