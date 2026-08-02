import yaml
import os
from typing import Dict, Any

class ImpactEstimator:
    """Estimates ATS score impact deterministically based on YAML weights."""
    
    def __init__(self, config_path: str = "config/impact_weights.yaml"):
        self.weights = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.weights = config.get("weights", {})
        else:
            # Fallback defaults
            self.weights = {
                "critical_skill": {"value": 8, "rationale": "Fallback critical skill"},
            }
            
    def estimate_impact(self, decision_category: str) -> int:
        """Returns the estimated ATS points gained for a decision category."""
        category_data = self.weights.get(decision_category, {"value": 1})
        return category_data.get("value", 1)

    def get_rationale(self, decision_category: str) -> str:
        """Returns the rationale for the weight configuration."""
        category_data = self.weights.get(decision_category, {"rationale": "General improvement"})
        return category_data.get("rationale", "General improvement")
