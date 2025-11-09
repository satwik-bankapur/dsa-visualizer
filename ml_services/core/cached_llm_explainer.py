# ml_services/core/cached_llm_explainer.py
import hashlib
import json
from functools import lru_cache
from ml_services.core.llm_explainer import LLMExplainer

class CachedLLMExplainer(LLMExplainer):
    """LLM Explainer with response caching for better performance"""

    def __init__(self, model: str = "codellama:7b-instruct"):
        super().__init__(model)
        self.cache = {}

    def generate_step_explanation(self, step_data, algorithm_pattern, problem_context):
        # Create cache key
        cache_key = self._create_cache_key(step_data, algorithm_pattern)

        if cache_key in self.cache:
            return self.cache[cache_key]

        # Generate new explanation
        explanation = super().generate_step_explanation(step_data, algorithm_pattern, problem_context)

        # Cache the result
        self.cache[cache_key] = explanation
        return explanation

    def _create_cache_key(self, step_data, algorithm_pattern):
        """Create unique cache key for step context"""
        key_data = {
            'code_line': step_data.get('code_line', ''),
            'pattern': algorithm_pattern,
            'changes': step_data.get('variable_changes', {})
        }
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
