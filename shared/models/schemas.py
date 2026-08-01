from pydantic import BaseModel, Field
from typing import List

class ATSFeedbackResponse(BaseModel):
    """
    Pydantic schema defining the exact JSON structure we expect the LLM to return.
    Updated for Phase 3 to provide more granular, section-by-section feedback.
    """
    
    ats_score: int = Field(
        ...,
        description="The overall ATS match score between 0 and 100."
    )
    
    summary: str = Field(
        ..., 
        description="A 2-3 sentence summary explaining why the resume is or isn't a good fit for the job."
    )
    
    missing_skills: List[str] = Field(
        ..., 
        description="A list of 3 to 7 crucial hard skills mentioned in the JD that are missing or weakly represented in the Resume."
    )
    
    project_feedback: List[str] = Field(
        ...,
        description="Actionable suggestions on how to improve the projects section."
    )
    
    experience_feedback: List[str] = Field(
        ...,
        description="Actionable suggestions on how to improve the work experience bullet points."
    )
    
    overall_feedback: str = Field(
        ...,
        description="General advice on formatting, keywords, and overall presentation."
    )
