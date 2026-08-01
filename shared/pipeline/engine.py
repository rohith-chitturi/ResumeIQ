from abc import ABC, abstractmethod
import time
from typing import List
from .context import PipelineContext
from .events import emitter, StageCompletedEvent, PipelineFailedEvent

class PipelineStage(ABC):
    """
    Extension API: Base interface for all pipeline processing stages.
    Implement this class to add new AI capabilities to the system.
    """
    
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    async def execute(self, context: PipelineContext) -> None:
        """
        Execute the stage logic. 
        Must mutate the context in-place.
        """
        pass


class Pipeline:
    """
    Lightweight Orchestrator. 
    Runs an array of PipelineStages sequentially over a unified PipelineContext.
    """
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    async def run(self, context: PipelineContext) -> PipelineContext:
        """Executes the pipeline stages and emits observability events."""
        try:
            for stage in self.stages:
                # Halt if a previous stage critically failed validation
                if not context.validation.is_valid:
                    break
                
                start_time = time.time()
                await stage.execute(context)
                duration_ms = (time.time() - start_time) * 1000
                
                # Emit event instead of tightly coupling to a logger/monitor
                await emitter.emit(
                    StageCompletedEvent(
                        context_id=context.id,
                        stage_name=stage.name,
                        duration_ms=duration_ms
                    )
                )
                
            return context
        except Exception as e:
            # Catch unhandled exceptions and bubble them up via events
            await emitter.emit(PipelineFailedEvent(context_id=context.id, error=str(e)))
            raise e
