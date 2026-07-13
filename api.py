from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import List, Optional

from parser.pdf_parser import PDFParser
from embedding.vectorizer import EmbeddingService
from similarity.matcher import SemanticMatcher
from llm.gemini_service import GeminiService
from models.schemas import ATSFeedbackResponse

app = FastAPI(title="ResumeIQ API", description="AI Resume Analyzer API", version="1.0.0")

# Enable CORS for the Stitch frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons for heavy models
embedding_service = EmbeddingService()
gemini_service = GeminiService()

class AnalyzeResponse(BaseModel):
    match_score: int
    feedback: Optional[ATSFeedbackResponse]

@app.get("/")
def read_root():
    return {"status": "ok", "message": "ResumeIQ API is running."}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyzes a PDF resume against a Job Description.
    """
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # Read the PDF bytes
        pdf_bytes = await resume.read()
        
        # Parse PDF
        resume_text = PDFParser.extract_text(pdf_bytes)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be scanned or corrupted.")
            
        # Calculate semantic match
        resume_emb = embedding_service.generate_embedding(resume_text)
        jd_emb = embedding_service.generate_embedding(job_description)
        score = SemanticMatcher.calculate_similarity(resume_emb, jd_emb)
        match_percent = int(score * 100)
        
        # Get AI ATS feedback
        feedback = None
        if gemini_service.client:
            feedback = gemini_service.analyze_resume(resume_text, job_description)
            
        return AnalyzeResponse(
            match_score=match_percent,
            feedback=feedback
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
