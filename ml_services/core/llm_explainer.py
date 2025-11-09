# ml_services/core/llm_explainer.py
import ollama
from typing import Dict, Any, Optional
from config.log_config import get_logger

logger = get_logger(__name__)

class LLMExplainer:
    """AI-powered explanation generator using local Ollama models"""

    def __init__(self, model: str = "codellama:7b-instruct"):
        self.model = model

    def get_explanation(self, prompt: str) -> str:
        """Get AI explanation from local LLM"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response['message']['content']

        except Exception as e:
            logger.error(f"LLM explanation failed: {e}")
            return "AI explanation unavailable."

    def generate_step_explanation(self,
                                  step_data: Dict[str, Any],
                                  algorithm_pattern: str,
                                  problem_context: str) -> str:
        """Generate context-aware explanation for a code execution step"""

        prompt = self._build_prompt(step_data, algorithm_pattern, problem_context)
        return self.get_explanation(prompt)

    def _build_prompt(self, step_data: Dict, pattern: str, context: str) -> str:
        """Build structured prompt for optimal LLM explanations"""

        prompt = f"""You are an expert programming tutor. Explain this algorithm step clearly and educationally.

Algorithm Pattern: {pattern}
Problem Context: {context}
Code Line: {step_data.get('code_line', '')}
Variable Changes: {step_data.get('variable_changes', {})}

Provide a clear, beginner-friendly explanation in 2-3 sentences that:
1. Describes what this step does
2. Explains why it's important for the algorithm
3. Connects it to the overall strategy

Explanation:"""

        return prompt
