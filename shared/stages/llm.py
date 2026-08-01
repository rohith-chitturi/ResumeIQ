from typing import Any
from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.llm.base import LLMProvider


class LLMStage(PipelineStage):
    """
    Executes the LLM generation based on the accumulated pipeline context.
    """
    def __init__(self, provider: LLMProvider, system_prompt: str):
        self.provider = provider
        self.system_prompt = system_prompt

    async def execute(self, context: PipelineContext) -> None:
        if not context.resume_text:
            context.fail_validation("LLMStage skipped: Missing resume_text.")
            return

        try:
            # Construct a rich prompt based on context
            user_prompt = f"Resume: {context.resume_text}\n"
            
            if context.company_profile:
                user_prompt += f"Target Company Profile: {context.company_profile}\n"
                
            if context.constraints:
                user_prompt += f"Missing Skills / Constraints to address: {context.constraints}\n"
            
            # Execute LLM call
            response = await self.provider.generate_async(self.system_prompt, user_prompt)
            
            # Update Context
            context.llm_output = response
            context.add_metric("llm_execution_count", 1.0)
            
        except Exception as e:
            context.fail_validation(f"LLMStage failed: {str(e)}")
