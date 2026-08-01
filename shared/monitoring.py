import time
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

class MetricsRegistry:
    """
    In-memory registry to track AI latencies for the current request.
    In a real system, this would push to Prometheus/Datadog.
    """
    
    def __init__(self):
        self.metrics = {}
        
    def record(self, name: str, duration_ms: float):
        self.metrics[name] = duration_ms
        logger.info(f"METRIC: {name} took {duration_ms:.2f}ms")

def track_latency(metric_name: str):
    """
    Decorator to track execution time of AI components.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            
            # If the instance has a metrics_registry, record it
            instance = args[0] if args else None
            if hasattr(instance, "metrics_registry"):
                instance.metrics_registry.record(metric_name, duration)
            else:
                logger.info(f"METRIC: {metric_name} took {duration:.2f}ms")
                
            return result
        return wrapper
    return decorator
