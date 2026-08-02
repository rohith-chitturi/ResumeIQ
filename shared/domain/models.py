from pydantic import BaseModel
from typing import List, Optional, Dict

class ConfidenceFactors(BaseModel):
    overall: float
    factors: Dict[str, float]

class Decision(BaseModel):
    decision_id: str
    category: str
    action: str
    priority: str
    rationale: str
    source: List[str]
    evidence: List[str]
    expected_impact: int
    confidence: ConfidenceFactors
    
    # Keeping a trace of the deterministic inputs for explainability
    trace: Optional[dict] = None
