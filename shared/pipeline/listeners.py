import logging
from shared.pipeline.events import (
    emitter, 
    StageCompletedEvent, 
    ValidationFailedEvent, 
    PipelineFailedEvent
)

logger = logging.getLogger("resumeiq.pipeline")


async def handle_stage_completed(event: StageCompletedEvent):
    """Logs metrics when a pipeline stage completes successfully."""
    logger.info(
        f"[Context: {event.context_id}] Stage '{event.stage_name}' "
        f"completed in {event.duration_ms:.2f}ms. Metadata: {event.metadata}"
    )


async def handle_validation_failed(event: ValidationFailedEvent):
    """Logs validation violations as warnings or alerts."""
    logger.warning(
        f"[Context: {event.context_id}] Validation FAILED at '{event.stage_name}'. "
        f"Errors: {event.errors}"
    )


async def handle_pipeline_failed(event: PipelineFailedEvent):
    """Logs critical, unhandled pipeline errors."""
    logger.error(
        f"[Context: {event.context_id}] CRITICAL PIPELINE FAILURE: {event.error}"
    )


def register_pipeline_listeners():
    """Subscribes the standard listeners to the global event emitter."""
    emitter.subscribe(StageCompletedEvent, handle_stage_completed)
    emitter.subscribe(ValidationFailedEvent, handle_validation_failed)
    emitter.subscribe(PipelineFailedEvent, handle_pipeline_failed)
    logger.info("Pipeline event listeners successfully registered.")
