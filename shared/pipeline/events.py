from abc import ABC
from datetime import datetime
from typing import Any, Callable, Dict, List
import asyncio


class PipelineEvent(ABC):
    """Base event for the pipeline architecture."""
    def __init__(self, context_id: str):
        self.context_id = context_id
        self.timestamp = datetime.utcnow()
        self.name = self.__class__.__name__


class StageCompletedEvent(PipelineEvent):
    """Emitted when a pipeline stage successfully completes."""
    def __init__(self, context_id: str, stage_name: str, duration_ms: float, metadata: Dict[str, Any] = None):
        super().__init__(context_id)
        self.stage_name = stage_name
        self.duration_ms = duration_ms
        self.metadata = metadata or {}


class ValidationFailedEvent(PipelineEvent):
    """Emitted when a pipeline validation stage fails."""
    def __init__(self, context_id: str, stage_name: str, errors: List[str]):
        super().__init__(context_id)
        self.stage_name = stage_name
        self.errors = errors


class PipelineFailedEvent(PipelineEvent):
    """Emitted when the entire pipeline fails due to an unhandled error."""
    def __init__(self, context_id: str, error: str):
        super().__init__(context_id)
        self.error = error


class EventEmitter:
    """Loosely coupled event publisher."""
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: type[PipelineEvent], listener: Callable):
        """Subscribe a listener to an event type."""
        event_name = event_type.__name__
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    async def emit(self, event: PipelineEvent):
        """Emit an event asynchronously to all registered listeners."""
        event_name = event.name
        listeners = self._listeners.get(event_name, [])
        
        # Fire and forget listeners using asyncio.create_task
        for listener in listeners:
            if asyncio.iscoroutinefunction(listener):
                asyncio.create_task(listener(event))
            else:
                listener(event)

# Global event emitter for the application lifecycle
emitter = EventEmitter()
