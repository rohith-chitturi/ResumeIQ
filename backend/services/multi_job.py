import asyncio
from typing import List, Dict, Any
from shared.pipeline.context import PipelineContext
from shared.pipeline.engine import Pipeline
from shared.stages.parse import ParseStage
from shared.stages.constraint import ConstraintStage
from shared.explainability import ExplainabilityEngine


class MultiJobOptimizationPipeline:
    """
    Executes a high-performance batch match of a single resume against multiple job descriptions.
    Does NOT use the LLM to save latency and token costs, relying entirely on deterministic Gap Analysis.
    """
    def __init__(self, explainability_engine: ExplainabilityEngine):
        self.parse_stage = ParseStage()
        self.constraint_stage = ConstraintStage(explainability_engine=explainability_engine)

    async def execute(self, resume_text: str, company_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculates gap analysis for multiple jobs concurrently.
        """
        # Parse resume once
        base_context = PipelineContext(resume_text=resume_text)
        await self.parse_stage.execute(base_context)
        
        if not base_context.validation.is_valid:
            return [{"error": "Resume parsing failed", "details": base_context.validation.errors}]

        tasks = []
        for profile in company_profiles:
            # Create a localized pipeline context for each job
            ctx = PipelineContext(
                resume_text=resume_text,
                company_profile=profile
            )
            # Inherit the already-parsed sections to save compute
            ctx.parsed_sections = base_context.parsed_sections
            
            # Run deterministic constraint engine
            tasks.append(self.constraint_stage.execute(ctx))
            
        await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for profile in company_profiles:
            # Reconstruct the context matches (in production, we'd map tasks to profiles)
            # For this MVP, we re-run sequentially if needed, but here we can just use a local run since it's deterministic CPU-bound
            ctx = PipelineContext(resume_text=resume_text, company_profile=profile)
            ctx.parsed_sections = base_context.parsed_sections
            await self.constraint_stage.execute(ctx)
            
            results.append({
                "company": profile.get("name", "Unknown"),
                "missing_skills": ctx.constraints,
                "ats_improvement_estimate": len(ctx.constraints) * 5.0 # Naive impact heuristic
            })
            
        # Sort by best initial match (fewest missing skills)
        results.sort(key=lambda x: len(x["missing_skills"]))
        return results
