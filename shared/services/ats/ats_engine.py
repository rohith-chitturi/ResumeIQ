from typing import Dict
from shared.services.parser.section_parser import SectionParser
from shared.services.embedding.vectorizer import EmbeddingService
from shared.services.similarity.matcher import SemanticMatcher
from shared.cache import CacheManager
import logging

logger = logging.getLogger(__name__)

class ATSEngine:
    """
    Computes explainable ATS scores by evaluating individual sections of the resume.
    """
    
    def __init__(self):
        self.embedder = EmbeddingService()
        
    def calculate_explainable_score(self, sections: Dict[str, str], job_description: str) -> Dict[str, float]:
        """
        Calculates match scores for each major section against the JD.
        """
        jd_emb = self.embedder.generate_embedding(job_description)
        
        scores = {}
        total_weight = 0
        weighted_sum = 0
        
        # Weights for each section
        weights = {
            "education": 0.1,
            "experience": 0.4,
            "skills": 0.3,
            "projects": 0.2
        }
        
        for sec, weight in weights.items():
            content = sections.get(sec, "").strip()
            if not content:
                scores[sec] = 0.0
                continue
                
            sec_emb = self.embedder.generate_embedding(content)
            score = SemanticMatcher.calculate_similarity(sec_emb, jd_emb)
            scores[sec] = round(score * 100, 2)
            
            weighted_sum += score * weight
            total_weight += weight
            
        overall_score = (weighted_sum / total_weight) * 100 if total_weight > 0 else 0
        scores["overall"] = round(overall_score, 2)
        
        return scores
