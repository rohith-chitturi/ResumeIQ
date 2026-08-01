from pydantic import BaseModel
from typing import List, Optional

class ExplainableScore(BaseModel):
    overall_score: float
    semantic_similarity: float
    ats_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    
class AIRecommendation(BaseModel):
    summary: str
    project_feedback: List[str]
    experience_feedback: List[str]
    overall_feedback: str

class FinalAnalysis(BaseModel):
    score: ExplainableScore
    recommendation: Optional[AIRecommendation]
