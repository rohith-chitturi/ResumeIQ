import asyncio
import copy
from typing import Dict, Any
from shared.pipeline.context import PipelineContext
from shared.pipeline.engine import Pipeline
from shared.stages.parse import ParseStage
from shared.stages.llm import LLMStage
from shared.stages.validation import ValidationStage
from shared.llm.base import LLMProvider


class SimulatorPipeline:
    """
    Executes the Recruiter Simulator workflow using three distinct personas.
    """
    def __init__(self, llm_provider: LLMProvider):
        self.provider = llm_provider
        self.parse_stage = ParseStage()
        
    def _create_persona_pipeline(self, persona_prompt: str) -> Pipeline:
        return Pipeline(
            stages=[
                LLMStage(provider=self.provider, system_prompt=persona_prompt),
                ValidationStage(require_json=True)
            ]
        )

    async def execute(self, resume_text: str, company_profile: dict) -> Dict[str, Any]:
        """
        Runs the simulator across ATS, Engineering Manager, and Recruiter personas.
        """
        base_context = PipelineContext(
            resume_text=resume_text,
            company_profile=company_profile
        )
        
        # Base parse step
        await self.parse_stage.execute(base_context)
        if not base_context.validation.is_valid:
            return {"error": base_context.validation.errors}

        # Define personas
        personas = {
            "ats_bot": "You are a strict ATS system. Extract keywords and return a match score (0-100) in JSON.",
            "eng_manager": "You are a pragmatic Engineering Manager. Critique the technical depth and impact in JSON.",
            "recruiter": "You are an HR Recruiter. Critique the formatting, clarity, and culture fit in JSON."
        }

        tasks = []
        persona_keys = list(personas.keys())
        
        for key in persona_keys:
            prompt = personas[key]
            # Copy context to avoid race conditions in parallel LLM/Validation stages
            ctx_copy = copy.deepcopy(base_context)
            pipeline = self._create_persona_pipeline(prompt)
            tasks.append(pipeline.run(ctx_copy))

        # Run LLM stages concurrently for performance
        results = await asyncio.gather(*tasks, return_exceptions=True)

        simulator_report = {}
        for idx, result in enumerate(results):
            key = persona_keys[idx]
            if isinstance(result, Exception):
                simulator_report[key] = {"error": str(result)}
            elif not result.validation.is_valid:
                simulator_report[key] = {"error": result.validation.errors}
            else:
                simulator_report[key] = result.llm_output

        return simulator_report
