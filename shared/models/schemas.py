from pydantic import BaseModel, Field
from typing import List

class ATSFeedbackResponse(BaseModel):
    """
    Pydantic schema defining the exact JSON structure we expect the Gemini LLM to return.
    
    Why use Pydantic for LLMs?
    - Historically, parsing LLM text output was a nightmare because the format was unpredictable.
    - With Structured Outputs (and Pydantic), we enforce a strict JSON schema.
    - If the LLM doesn't return this exact format, the API call fails or the SDK parses it automatically into this Python object.
    
    This guarantees our Streamlit UI won't crash when trying to access `missing_skills` or `bullet_point_improvements`.
    """
    
    match_summary: str = Field(
        ..., 
        description="A 2-3 sentence summary explaining why the resume is or isn't a good fit for the job."
    )
    
    missing_skills: List[str] = Field(
        ..., 
        description="A list of 3 to 7 crucial hard skills mentioned in the JD that are missing or weakly represented in the Resume."
    )
    
    bullet_point_improvements: List[str] = Field(
        ..., 
        description="A list of 2 to 4 actionable suggestions on how to rewrite specific bullet points to better align with the JD, using the XYZ format (Accomplished [X] as measured by [Y], by doing [Z])."
    )
