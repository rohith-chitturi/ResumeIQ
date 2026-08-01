from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import time

from shared.orchestrator import AIOrchestrator
from shared.logs.logger import logger
from backend.config.settings import settings
from backend.db.repository import get_db

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
orchestrator = AIOrchestrator()

class AnalysisResult(BaseModel):
    ats_scores: Dict[str, float]
    feedback: Optional[Dict[str, Any]]
    parsed_sections: Dict[str, str]
    metrics: Dict[str, float]

@app.get("/")
def health_check():
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} API running."}

@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db=Depends(get_db) # DB injected for future persistence
):
    """
    Production endpoint for end-to-end resume analysis.
    """
    logger.info(f"Received analysis request for {resume.filename}")
    
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    start_time = time.time()
    
    try:
        pdf_bytes = await resume.read()
        
        # The orchestrator handles the entire flow
        result = orchestrator.process_resume(pdf_bytes, job_description)
        
        total_time = (time.time() - start_time) * 1000
        
        return AnalysisResult(
            ats_scores=result["ats_scores"],
            feedback=result["feedback"],
            parsed_sections=result["parsed_sections"],
            metrics={"total_latency_ms": total_time}
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000)
