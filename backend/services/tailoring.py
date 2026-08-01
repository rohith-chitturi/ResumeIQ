from shared.pipeline.context import PipelineContext
from shared.pipeline.engine import Pipeline
from shared.stages.parse import ParseStage
from shared.stages.constraint import ConstraintStage
from shared.stages.retrieve import RetrieveStage
from shared.stages.llm import LLMStage
from shared.stages.validation import ValidationStage
from shared.llm.base import LLMProvider
from shared.explainability import ExplainabilityEngine

class ResumeTailoringPipeline:
    """
    Executes the Resume Tailoring workflow using the generalized AI Pipeline Framework.
    """
    def __init__(self, llm_provider: LLMProvider, explainability_engine: ExplainabilityEngine, retriever):
        self.pipeline = Pipeline(
            stages=[
                ParseStage(),
                ConstraintStage(explainability_engine=explainability_engine),
                RetrieveStage(retriever=retriever),
                LLMStage(
                    provider=llm_provider,
                    system_prompt=(
                        "You are an expert technical recruiter. Re-write the provided resume "
                        "to explicitly address the Missing Skills / Constraints while keeping the tone professional. "
                        "Crucially, adhere to the retrieved 'Reference Knowledge' best practices. "
                        "Return your output as a valid JSON object with a 'tailored_resume' key."
                    )
                ),
                ValidationStage(require_json=True)
            ]
        )

    async def execute(self, resume_text: str, company_profile: dict) -> PipelineContext:
        """
        Runs the tailoring pipeline and returns the resulting context.
        """
        context = PipelineContext(
            resume_text=resume_text,
            company_profile=company_profile
        )
        
        # The pipeline handles all execution, error catching, event emitting, and metrics
        return await self.pipeline.run(context)
