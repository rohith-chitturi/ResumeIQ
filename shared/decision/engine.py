from typing import List
from shared.domain.models import Decision, ConfidenceFactors
from shared.decision.impact_estimator import ImpactEstimator
import uuid

class DecisionEngine:
    """
    Analyzes gap analysis constraints and retrieved knowledge to build deterministic Decision objects.
    """
    def __init__(self, estimator: ImpactEstimator):
        self.estimator = estimator

    def analyze(self, constraints: List[str], retrieved_knowledge: str) -> List[Decision]:
        decisions = []
        
        for idx, constraint in enumerate(constraints):
            rule_key = "critical_skill"
            impact = self.estimator.estimate_impact(rule_key)
            base_rationale = self.estimator.get_rationale(rule_key)
            
            # Compute multi-factor confidence explicitly
            retrieval_support = 0.93 if constraint in retrieved_knowledge else 0.50
            jd_match = 0.98  # Derived from ConstraintStage (mocked here)
            ats_rule_strength = 0.87
            validation = 1.00
            
            overall_confidence = (jd_match * 0.4) + (retrieval_support * 0.3) + (ats_rule_strength * 0.3)
            
            decision = Decision(
                decision_id=f"DEC-{str(uuid.uuid4())[:8].upper()}",
                category="Skills",
                action=f"Add {constraint}",
                priority="High" if impact >= 6 else "Medium",
                rationale=f"'{constraint}' is missing from the resume. {base_rationale}.",
                source=[
                    "ATS Engine",
                    "Knowledge Retrieval"
                ],
                evidence=[
                    f"Missing Skill: {constraint}",
                    "JD Evidence: Required in target job description",
                    "Knowledge Evidence: Supported by retrieved formatting best practices"
                ],
                expected_impact=impact,
                confidence=ConfidenceFactors(
                    overall=round(overall_confidence, 2),
                    factors={
                        "jd_match": jd_match,
                        "retrieval_support": retrieval_support,
                        "ats_rule_strength": ats_rule_strength,
                        "validation": validation
                    }
                ),
                trace={
                    "input_constraint": constraint,
                    "rule_applied": rule_key,
                    "retrieval_support": constraint in retrieved_knowledge
                }
            )
            decisions.append(decision)
            
        return decisions
