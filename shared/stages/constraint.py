from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.explainability import ExplainabilityEngine


class ConstraintStage(PipelineStage):
    """
    Computes constraints (missing skills, gaps) between the Resume and CompanyProfile.
    """
    def __init__(self, explainability_engine: ExplainabilityEngine = None):
        self.engine = explainability_engine or ExplainabilityEngine()

    async def execute(self, context: PipelineContext) -> None:
        if not context.company_profile:
            context.fail_validation("ConstraintStage skipped: No company_profile in context.")
            return

        if not context.parsed_sections:
            context.fail_validation("ConstraintStage skipped: No parsed_sections in context.")
            return

        try:
            # Extract skills from the parsed resume
            # Assume a simple concatenation for the engine
            resume_text = " ".join(context.parsed_sections.values())
            resume_skills = self.engine._extract_skills(resume_text)
            
            # Extract required skills from the company profile
            required_skills = set(context.company_profile.get("keywords", []))
            
            # Calculate gap (constraints)
            missing_skills = list(required_skills - resume_skills)
            
            context.constraints = missing_skills
            context.add_metric("missing_skills_count", len(missing_skills))
            
        except Exception as e:
            context.fail_validation(f"ConstraintStage failed: {str(e)}")
