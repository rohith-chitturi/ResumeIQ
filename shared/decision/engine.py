from typing import List
from shared.domain.models import Decision
from shared.decision.impact_estimator import ImpactEstimator

class DecisionEngine:
    """
    Analyzes gap analysis constraints and retrieved knowledge to build deterministic Decision objects.
    """
    def __init__(self, estimator: ImpactEstimator):
        self.estimator = estimator

    def analyze(self, constraints: List[str], retrieved_knowledge: str) -> List[Decision]:
        decisions = []
        
        # In a real system, we would parse the retrieved knowledge and cross-reference with JD keywords
        for constraint in constraints:
            # Example rule: missing a constraint is a critical skill gap
            impact = self.estimator.estimate_impact("critical_skill")
            
            decision = Decision(
                category="Skills",
                action=f"Add {constraint}",
                priority="High" if impact >= 6 else "Medium",
                rationale=f"'{constraint}' is missing from the resume but required by the target job.",
                evidence=[
                    f"Identified in Gap Analysis",
                    "Improves ATS keyword coverage"
                ],
                expected_impact=impact,
                confidence=0.95, # Deterministically very high for missing JD constraints
                trace={
                    "input_constraint": constraint,
                    "rule_applied": "critical_skill",
                    "retrieval_support": constraint in retrieved_knowledge
                }
            )
            decisions.append(decision)
            
        return decisions
