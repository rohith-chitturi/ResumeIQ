from shared.pipeline.context import PipelineContext
from shared.pipeline.engine import Pipeline
from shared.stages.parse import ParseStage
from shared.stages.constraint import ConstraintStage
from shared.stages.llm import LLMStage
from shared.stages.validation import ValidationStage
from shared.llm.base import LLMProvider
from shared.explainability import ExplainabilityEngine

class InterviewPrepPipeline:
    """
    Executes the Interview Readiness workflow.
    Generates technical and behavioral questions based on missing skills.
    """
    def __init__(self, llm_provider: LLMProvider, explainability_engine: ExplainabilityEngine):
        self.pipeline = Pipeline(
            stages=[
                ParseStage(),
                ConstraintStage(explainability_engine=explainability_engine),
                LLMStage(
                    provider=llm_provider,
                    system_prompt=(
                        "You are an expert technical interviewer. Based on the candidate's resume "
                        "and the missing skills/constraints identified for the target role, generate "
                        "3 technical questions and 2 behavioral questions. "
                        "Format output as a JSON object with 'technical' and 'behavioral' arrays, "
                        "where each object has a 'question' and 'difficulty_level' key."
                    )
                ),
                ValidationStage(require_json=True)
            ]
        )

    async def execute(self, resume_text: str, company_profile: dict) -> PipelineContext:
        """
        Runs the interview prep pipeline.
        """
        context = PipelineContext(
            resume_text=resume_text,
            company_profile=company_profile
        )
        return await self.pipeline.run(context)
