from typing import Dict, Any
from shared.services.parser.pdf_parser import PDFParser
from shared.services.parser.section_parser import SectionParser
from shared.services.ats.ats_engine import ATSEngine
from shared.services.llm.gemini_service import GeminiService
import logging

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    Coordinates the entire AI pipeline:
    Resume -> Parser -> Section Parser -> ATS Engine -> Prompt -> LLM
    """
    
    def __init__(self):
        self.ats_engine = ATSEngine()
        self.llm_service = GeminiService()
        
    def process_resume(self, pdf_bytes: bytes, job_description: str) -> Dict[str, Any]:
        """
        Executes the full pipeline and returns structured data.
        """
        logger.info("Starting AI Orchestrator pipeline")
        
        # 1. Parse PDF
        raw_text = PDFParser.extract_text_from_bytes(pdf_bytes)
        if not raw_text:
            raise ValueError("Failed to extract text from PDF")
            
        # 2. Section Parsing
        sections = SectionParser.parse_sections(raw_text)
        
        # 3. Explainable ATS Scoring
        ats_scores = self.ats_engine.calculate_explainable_score(sections, job_description)
        
        # 4. LLM Analysis
        feedback = self.llm_service.analyze_resume(raw_text, job_description)
        
        return {
            "ats_scores": ats_scores,
            "feedback": feedback.model_dump() if feedback else None,
            "parsed_sections": sections
        }
