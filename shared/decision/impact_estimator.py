import yaml
import os

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
                "critical_skill": 8,
                "preferred_skill": 4,
                "project_alignment": 6,
                "formatting": 2
            }
            
    def estimate_impact(self, decision_category: str) -> int:
        """Returns the estimated ATS points gained for a decision category."""
        return self.weights.get(decision_category, 1)
