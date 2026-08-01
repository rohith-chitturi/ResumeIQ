from typing import List, Dict, Any
from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """
    Offline evaluation abstraction for benchmarking AI quality.
    """
    @abstractmethod
    def evaluate(self, input_context: Any, llm_output: Any) -> Dict[str, float]:
        """Returns a mapping of metric names to scores (0.0 to 1.0)."""
        pass


class ConstraintEvaluator(BaseEvaluator):
    """
    Evaluates whether the LLM output successfully addressed all constraints.
    """
    def evaluate(self, input_context: Any, llm_output: Any) -> Dict[str, float]:
        if not hasattr(input_context, 'constraints') or not input_context.constraints:
            return {"constraint_satisfaction_rate": 1.0}

        constraints: List[str] = input_context.constraints
        output_str = str(llm_output).lower()

        satisfied = 0
        for constraint in constraints:
            if constraint.lower() in output_str:
                satisfied += 1
                
        satisfaction_rate = satisfied / len(constraints) if constraints else 1.0
        
        return {
            "constraint_satisfaction_rate": satisfaction_rate,
            "missed_constraints_count": float(len(constraints) - satisfied)
        }


class JSONSchemaEvaluator(BaseEvaluator):
    """
    Evaluates how often the LLM returns well-formed JSON without markdown stripping.
    """
    def evaluate(self, input_context: Any, llm_output: Any) -> Dict[str, float]:
        if isinstance(llm_output, dict):
            return {"native_json_success": 1.0}
        
        if isinstance(llm_output, str) and llm_output.strip().startswith("{"):
            return {"native_json_success": 0.8} # Valid string JSON but not parsed natively
            
        return {"native_json_success": 0.0}
