# Agentic HR Screening System API

This project is a sophisticated, agentic AI system designed to automate the initial phases of the HR recruitment process. It uses a multi-agent approach with Large Language Models (LLMs) to parse job descriptions, screen candidate resumes, and provide a ranked shortlist of suitable candidates.

![System Architecture](architecture.png)

---

## 🌟 Key Features

- **Multi-Agent Architecture**: Separate agents for parsing, screening, and matching, allowing for specialized and robust logic.
- **Intelligent Parsing**: Uses an LLM (Google Gemini) to extract structured data from unstructured job descriptions and resumes.
- **Ethical by Design**: Implements automatic PII (Personally Identifiable Information) masking to ensure candidate privacy and PDPA/GDPR compliance.
- **Database Integration**: Stores job and candidate data in a relational database (SQLite) using SQLModel.
- **Performance Optimized**: Features a built-in cache to dramatically speed up repeated LLM calls, saving time and cost.
- **API-driven**: The entire system is exposed via a professional FastAPI web server with automated documentation.
- **Containerized**: Packaged with Docker for easy, consistent, and portable deployment.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **AI/LLM**: LangChain, Google Gemini-2.0-Flash
- **Database**: SQLModel, SQLAlchemy, SQLite
- **DevOps**: Docker, Docker Compose
- **Tooling**: Pydantic, Presidio for PII masking

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- A Google Gemini API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/hr-agentic-ai-project.git
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

The API will be available at `http://127.0.0.1:8000`.

---

## Usage

The best way to interact with the API is through the auto-generated documentation.

1.  Navigate to **`http://127.0.0.1:8000/docs`** in your browser.

2.  Use the `POST /screen/{job_id}` endpoint to run the screening pipeline.
    -   Try `job_id: 1` to screen for the "Senior Python Developer" role.
    -   The system will process the applicants from the database and return a ranked JSON report.

### Example Response

```json
{
  "job_title": "Senior Python Developer",
  "ranked_candidates": [
    {
      "candidate_id": "CAND_1",
      "score": 9,
      "justification": "Excellent match. Exceeds experience requirement and possesses all key skills including FastAPI and Docker."
    },
    // ... other candidates
  ]
}