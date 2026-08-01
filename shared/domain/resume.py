from pydantic import BaseModel
from typing import Dict, Optional

class ParsedResume(BaseModel):
    """Domain model representing a parsed resume."""
    filename: str
    raw_text: str
    sections: Dict[str, str]

class AnalysisRequest(BaseModel):
    """Domain model for a single analysis request."""
    resume: ParsedResume
    job_description: str
