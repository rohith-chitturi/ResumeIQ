from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.decision.engine import DecisionEngine

class DecisionStage(PipelineStage):
    """
    Executes the Decision Intelligence Engine.
    Converts constraints and knowledge into deterministic Decision objects before passing to the LLM.
    """
    def __init__(self, decision_engine: DecisionEngine):
        self.decision_engine = decision_engine

    async def execute(self, context: PipelineContext) -> None:
        try:
            # Generate deterministic decisions based on constraints
            decisions = self.decision_engine.analyze(
                constraints=context.constraints,
                retrieved_knowledge=context.retrieved_knowledge
            )
            
            # Sort decisions by expected impact
            decisions.sort(key=lambda d: d.expected_impact, reverse=True)
            
            context.decisions = decisions
            context.add_metric("decision_count", len(decisions))
            
        except Exception as e:
            context.fail_validation(f"DecisionStage failed: {str(e)}")
