import json
from shared.pipeline.engine import PipelineStage
from shared.pipeline.context import PipelineContext
from shared.pipeline.events import emitter, ValidationFailedEvent


class ValidationStage(PipelineStage):
    """
    Validates LLM outputs against required schemas, business rules, and safety constraints.
    """
    def __init__(self, require_json: bool = True):
        self.require_json = require_json

    async def execute(self, context: PipelineContext) -> None:
        if not context.llm_output:
            context.fail_validation("ValidationStage failed: No LLM output to validate.")
            return

        try:
            # 1. Safety Validation (Basic injection check)
            if "ignore all previous instructions" in str(context.llm_output).lower():
                context.fail_validation("Safety violation: Potential prompt injection detected.")
                
            # 2. Schema Validation (JSON parseable if required)
            if self.require_json and isinstance(context.llm_output, str):
                try:
                    # Strip markdown blocks if present
                    raw_text = context.llm_output
                    if raw_text.startswith("```json"):
                        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                        
                    parsed_json = json.loads(raw_text)
                    context.llm_output = parsed_json
                    context.add_metric("json_validation_success", 1.0)
                except json.JSONDecodeError:
                    context.fail_validation("Schema violation: LLM output is not valid JSON.")
                    context.add_metric("json_validation_success", 0.0)

            # If validation failed during this stage, emit event
            if not context.validation.is_valid:
                await emitter.emit(
                    ValidationFailedEvent(
                        context_id=context.id,
                        stage_name=self.name,
                        errors=context.validation.errors
                    )
                )

        except Exception as e:
            context.fail_validation(f"ValidationStage critically failed: {str(e)}")
