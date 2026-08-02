import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from shared.domain.models import Decision


class ValidationState(BaseModel):
    """Tracks the validation state of the context."""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)


class PipelineContext(BaseModel):
    """
    Unified state object that flows sequentially through pipeline stages.
    Prevents parameter bloat and tightly couples related AI data.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Input Data
    resume_text: Optional[str] = None
    job_description_text: Optional[str] = None
    company_profile: Optional[Dict[str, Any]] = None
    
    # Intermediate Processing Data
    parsed_sections: Dict[str, str] = Field(default_factory=dict)
    embeddings: Dict[str, List[float]] = Field(default_factory=dict)
    ats_score: Optional[float] = None
    constraints: List[str] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    
    # Output Data
    retrieved_knowledge: str = ""
    llm_output: Optional[Any] = None
    confidence_score: float = 0.0
    
    # Execution State
    validation: ValidationState = Field(default_factory=ValidationState)
    metrics: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_metric(self, key: str, value: float):
        """Helper to add operational metrics (e.g., latency, token count)."""
        self.metrics[key] = value

    def fail_validation(self, error: str):
        """Helper to mark validation failure and halt subsequent processing (if applicable)."""
        self.validation.is_valid = False
        self.validation.errors.append(error)
