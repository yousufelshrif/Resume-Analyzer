# Resume Analyzer

A lightweight FastAPI service that compares a resume with a target job description and returns a match score with feedback. The API accepts PDF or DOCX resumes, extracts their text, parses the resume and job description, and evaluates their alignment.

## What it does

- Accepts a resume file and job description through a multipart form request
- Extracts resume text and parses resume and job information
- Computes a matching score and generates feedback
- Returns the results as JSON
- Provides a simple health-check endpoint

## How the request flows

1. Upload a resume and provide the target job description.
2. The service extracts text from the resume.
3. Resume and job details are parsed.
4. The matching score and feedback are calculated and returned.

## Technology

- Python
- FastAPI
- Resume and job-description extraction
- JSON API responses

## Run locally

From the repository root:

```bash
python -m pip install -r requirements.txt
uvicorn ai.source.main:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The root endpoint, `GET /`, returns a basic service status.

## API

### `POST /score`

Send a multipart form request with:

| Field | Type | Description |
| --- | --- | --- |
| `resume_file` | File | Resume in PDF or DOCX format |
| `job_description` | Text | The job description to compare against |

The response is JSON with a `score` and `feedback` field. See the interactive API documentation for the exact response produced by the current code.

## Project structure

```text
ai/
├── extractors/       # Resume, job, and text extraction
├── scoring.py        # Matching score and feedback logic
└── source/
    └── main.py       # FastAPI application and API routes
```

## Scope and limitations

This repository provides an API prototype, not a complete job-search product or a hiring decision system. Treat its score and feedback as decision-support signals: review the underlying resume and job requirements yourself. Before deploying publicly, review the API’s CORS settings, file validation, error handling, and data-retention practices.

## Privacy

Resumes contain sensitive personal information. Use test files when evaluating the project, obtain permission before processing someone else’s resume, and avoid logging or sharing uploaded documents.

## Project status

Portfolio project. The README describes the behavior implemented in the repository; deployment, accuracy, and production-readiness claims are intentionally not implied.
