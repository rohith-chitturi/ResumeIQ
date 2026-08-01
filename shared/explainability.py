from typing import Dict, List, Set
from shared.domain.analysis import ExplainableScore

class ExplainabilityEngine:
    """
    Deterministically computes explainable metrics (matched skills, missing skills)
    without relying on an LLM, reducing latency and cost.
    """
    
    @staticmethod
    def extract_skills_from_text(text: str) -> Set[str]:
        # Stub: A real implementation would use spaCy or a predefined skill ontology
        skills = {"python", "fastapi", "docker", "kubernetes", "aws", "react", "sql"}
        found = set()
        text_lower = text.lower()
        for skill in skills:
            if skill in text_lower:
                found.add(skill)
        return found
        
    def generate_metrics(
        self, 
        resume_text: str, 
        jd_text: str, 
        semantic_similarity: float, 
        ats_score: float
    ) -> ExplainableScore:
        
        resume_skills = self.extract_skills_from_text(resume_text)
        jd_skills = self.extract_skills_from_text(jd_text)
        
        matched = list(resume_skills.intersection(jd_skills))
        missing = list(jd_skills.difference(resume_skills))
        
        overall_score = (0.70 * semantic_similarity) + (0.30 * ats_score)
        
        strengths = []
        if len(matched) > 3:
            strengths.append("Strong technical skill overlap.")
        if ats_score > 80:
            strengths.append("Excellent formatting and structure.")
            
        weaknesses = []
        if missing:
            weaknesses.append(f"Missing core requirements: {', '.join(missing[:3])}")
            
        return ExplainableScore(
            overall_score=round(overall_score, 2),
            semantic_similarity=round(semantic_similarity, 2),
            ats_score=round(ats_score, 2),
            matched_skills=matched,
            missing_skills=missing,
            strengths=strengths,
            weaknesses=weaknesses
        )
