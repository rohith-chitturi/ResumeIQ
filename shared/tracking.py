import os
import json
from datetime import datetime
from typing import Dict, Any


class ExperimentTracker:
    """
    Lightweight MLOps tracker for offline evaluation benchmarking.
    Outputs metrics and errors into the experiments/ directory for reproducible research.
    """
    def __init__(self, run_name_prefix: str = "run"):
        timestamp = datetime.utcnow().strftime("%Y_%m_%d_%H%M%S")
        self.run_id = f"{run_name_prefix}_{timestamp}"
        self.run_dir = os.path.join("experiments", self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)
        
    def log_metrics(self, metrics: Dict[str, float]):
        """Saves aggregate benchmarks (e.g. Recall@5, latency)."""
        filepath = os.path.join(self.run_dir, "metrics.json")
        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=4)
            
    def log_errors(self, errors: Dict[str, Any]):
        """Saves validation failures and wrong retrievals for Error Analysis."""
        filepath = os.path.join(self.run_dir, "errors.json")
        with open(filepath, "w") as f:
            json.dump(errors, f, indent=4)
