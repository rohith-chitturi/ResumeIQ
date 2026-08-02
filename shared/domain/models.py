from pydantic import BaseModel
from typing import List, Optional

class Decision(BaseModel):
    category: str
    action: str
    priority: str
    rationale: str
    evidence: List[str]
    expected_impact: int
    confidence: float
    
    # Keeping a trace of the deterministic inputs for explainability
    trace: Optional[dict] = None
