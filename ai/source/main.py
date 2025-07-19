import os
import sys
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile
import shutil
from fastapi.middleware.cors import CORSMiddleware


# Get the absolute path of the project root directory (parent of 'ai' directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import your modules
from ai.extractors.text_extractor import ResumeTextExtractor
from ai.extractors.resume.resume_extractor import ResumeExtractor
from ai.extractors.job.job_extractor import JobExtractor
from ai.scoring import compute_matching_score, generate_feedback

app = FastAPI(title="Resume Analyzer API")

# Allow all origins that contain 'localhost' or '127.0.0.1'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/score")
async def score_resume(
    resume_file: UploadFile = File(..., description="Resume file in PDF or DOCX format"),
    job_description: str = Form(..., description="Job description text")
):
    # Save uploaded resume to a temporary file
    suffix = os.path.splitext(resume_file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(resume_file.file, tmp)
        tmp_path = tmp.name

    try:
        # 1. Extract resume text
        extractor = ResumeTextExtractor(tmp_path)
        resume_text = extractor.extract_text()
        # 2. Parse job description
        job_parser = JobExtractor()
        job_data = job_parser.parse(job_description)

        # 3. Parse resume content
        resume_parser = ResumeExtractor()
        resume_data = resume_parser.parse(resume_text)
    
        # 4. Compute matching score
        score = compute_matching_score(resume_data, job_data)
        feedback = generate_feedback(resume_data, job_data)

        # Return JSON response
        return JSONResponse({
            "score": round(score, 2),
            "feedback": feedback
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        # Clean up temporary file
        os.remove(tmp_path)

# Optional health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok"}

# To run locally:
# uvicorn source.main:app --reload --host 0.0.0.0 --port 8000
