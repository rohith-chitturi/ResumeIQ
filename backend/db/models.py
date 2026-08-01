from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from backend.db.repository import Base

class ResumeAnalysis(Base):
    """
    SQLAlchemy model for storing parsed resumes, their vectors, and ATS feedback.
    This enables future "resume search" functionality using pgvector.
    """
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    job_description = Column(String)
    
    # Core extracted text
    parsed_text = Column(String)
    
    # Store the 384-dimensional vector from our all-MiniLM-L6-v2 embedding model
    embedding = Column(Vector(384))
    
    # Overall Score computed by ATS Engine
    ats_score = Column(Integer)
    
    # Metadata and tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
