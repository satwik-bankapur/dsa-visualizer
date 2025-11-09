# ml_services/core/step_explainer.py
import hashlib
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from core.execution_tracker import ExecutionStep
from models.internal_models import AlgorithmPattern
from config.log_config import get_logger

logger = get_logger(__name__)

# Try to import ollama, fallback if not available
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama not available, using fallback explanations")

@dataclass
class PromptTemplate:
    """Template for generating LLM prompts"""
    system_template: str
    user_template: str = ""

    def format_prompt(self, code_line: str = "", variable_changes: str = "") -> str:
        """Format the complete prompt with sanitized variables"""
        # Sanitize inputs to prevent format string attacks
        safe_code = str(code_line).replace('{', '{{').replace('}', '}}')
        safe_changes = str(variable_changes).replace('{', '{{').replace('}', '}}')
        return f"{self.system_template}\n\nCode: {safe_code}\nChanges: {safe_changes}"

class StepExplainer:
    """AI-Enhanced step explainer using local LLM (Ollama)"""

    def __init__(self, model_name: str = "codellama:7b-instruct"):
        self.model_name = model_name
        self.explanation_cache = {}
        self.algorithm_prompts = self._initialize_algorithm_prompts()
        self.fallback_explainer = FallbackStepExplainer()

    def _initialize_algorithm_prompts(self) -> Dict[AlgorithmPattern, PromptTemplate]:
        """Initialize algorithm-specific prompt templates"""
        return {
            AlgorithmPattern.HASH_MAP: PromptTemplate(
                system_template="Explain hash map step in 1 sentence, max 15 words. Be direct."
            ),
            AlgorithmPattern.TWO_POINTERS: PromptTemplate(
                system_template="Explain two pointers step in 1 sentence, max 15 words. Be direct."
            ),
            AlgorithmPattern.SLIDING_WINDOW: PromptTemplate(
                system_template="Explain sliding window step in 1 sentence, max 15 words. Be direct."
            ),
            AlgorithmPattern.BINARY_SEARCH: PromptTemplate(
                system_template="Explain binary search step in 1 sentence, max 15 words. Be direct."
            ),
            AlgorithmPattern.DEPTH_FIRST_SEARCH: PromptTemplate(
                system_template="Explain DFS step in 1 sentence, max 15 words. Be direct."
            ),
            AlgorithmPattern.DYNAMIC_PROGRAMMING: PromptTemplate(
                system_template="Explain DP step in 1 sentence, max 15 words. Be direct."
            )
        }

    def enhance_steps_with_explanations(
            self,
            steps: List[ExecutionStep],
            algorithm_pattern: AlgorithmPattern,
            problem_context: Dict[str, Any]
    ) -> List[ExecutionStep]:
        """Add AI-enhanced educational explanations to execution steps"""
        enhanced_steps = []

        for step in steps:
            # Create enhanced step
            enhanced_step = ExecutionStep(
                step_number=step.step_number,
                code_line=step.code_line,
                variable_changes=step.variable_changes,
                variables_before=getattr(step, 'variables_before', {}),
                variables_after=getattr(step, 'variables_after', {}),
                event_type=getattr(step, 'event_type', 'execution'),
                explanation="",
                visualization_data={}
            )

            if self._should_explain_step(enhanced_step, algorithm_pattern):
                try:
                    enhanced_step.explanation = self._generate_ai_explanation(
                        enhanced_step, algorithm_pattern, problem_context
                    )
                except Exception as e:
                    logger.warning(f"AI explanation failed for step {step.step_number}: {e}")
                    enhanced_step.explanation = self._generate_fallback_explanation(
                        enhanced_step, algorithm_pattern
                    )
            else:
                enhanced_step.explanation = self._generate_fallback_explanation(
                    enhanced_step, algorithm_pattern
                )

            enhanced_step.visualization_data = self._generate_visualization_data(
                enhanced_step, algorithm_pattern
            )
            enhanced_steps.append(enhanced_step)

        logger.info(f"Enhanced {len(enhanced_steps)} steps with explanations")
        return enhanced_steps

    def _generate_ai_explanation(
            self,
            step: ExecutionStep,
            pattern: AlgorithmPattern,
            context: Dict[str, Any]
    ) -> str:
        """Generate AI explanation using algorithm-specific prompts"""
        if not OLLAMA_AVAILABLE:
            raise Exception("Ollama not available")

        cache_key = self._create_cache_key(step, pattern)
        if cache_key in self.explanation_cache:
            return self.explanation_cache[cache_key]

        prompt_template = self.algorithm_prompts.get(
            pattern,
            PromptTemplate(system_template="Explain in 1 sentence, max 15 words. Be direct.")
        )

        prompt = prompt_template.format_prompt(
            code_line=step.code_line.strip(),
            variable_changes=self._format_variable_changes(step.variable_changes)
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.1,
                    "max_tokens": 25,
                    "top_p": 0.7,
                    "stop": ["\n", ".", "!", "?"]
                }
            )

            explanation = self._trim_explanation(response['message']['content'].strip())
            self.explanation_cache[cache_key] = explanation
            return explanation

        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            raise

    def _generate_fallback_explanation(
            self,
            step: ExecutionStep,
            pattern: AlgorithmPattern
    ) -> str:
        """Generate concise fallback explanation when AI fails"""
        code_line = step.code_line.strip().lower()

        # Algorithm-specific explanations
        if pattern == AlgorithmPattern.HASH_MAP:
            if 'complement' in code_line:
                return "Calculate complement for target sum"
            elif 'in ' in code_line and ('map' in code_line or 'dict' in code_line):
                return "Check if complement exists in hash map"
            elif '{}' in code_line or 'dict(' in code_line:
                return "Initialize empty hash map"
            elif '[' in code_line and '=' in code_line:
                return "Store value-index pair in hash map"
            return "Hash map operation for O(1) lookup"

        elif pattern == AlgorithmPattern.TWO_POINTERS:
            if 'left' in code_line and '+' in code_line:
                return "Move left pointer forward"
            elif 'right' in code_line and '-' in code_line:
                return "Move right pointer backward"
            elif 'left' in code_line and 'right' in code_line:
                return "Compare values at both pointers"
            return "Two pointers technique step"

        elif pattern == AlgorithmPattern.BINARY_SEARCH:
            if 'mid' in code_line:
                return "Calculate middle index for binary search"
            elif 'left' in code_line or 'low' in code_line:
                return "Update left search boundary"
            elif 'right' in code_line or 'high' in code_line:
                return "Update right search boundary"
            return "Binary search step"

        elif pattern == AlgorithmPattern.SLIDING_WINDOW:
            if 'start' in code_line or 'left' in code_line:
                return "Adjust window start position"
            elif 'end' in code_line or 'right' in code_line:
                return "Expand window to right"
            return "Sliding window adjustment"

        # Generic fallbacks
        if 'return' in code_line:
            return "Return solution"
        elif 'if' in code_line:
            return "Check condition"
        elif 'while' in code_line or 'for' in code_line:
            return "Loop iteration"
        elif '=' in code_line:
            return "Update variable"

        return "Execute algorithm step"

    def _should_explain_step(self, step: ExecutionStep, pattern: AlgorithmPattern) -> bool:
        """Determine if step needs explanation"""
        code_line = step.code_line.strip()

        # Skip empty lines and comments
        if not code_line or code_line.startswith('#'):
            return False

        # Skip trivial assignments for loop counters
        if len(code_line) < 5 and any(var in code_line for var in ['i++', 'j++', 'k++']):
            return False

        return True

    def _create_cache_key(self, step: ExecutionStep, pattern: AlgorithmPattern) -> str:
        """Create secure cache key using SHA256"""
        key_data = f"{step.code_line}_{pattern.value}_{len(step.variable_changes)}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]

    def _format_variable_changes(self, changes: Dict[str, Any]) -> str:
        """Format variable changes safely"""
        if not changes:
            return "No changes"

        formatted = []
        for var, value in list(changes.items())[:3]:  # Limit to 3 changes
            safe_var = str(var)[:20]
            safe_value = str(value)[:30]
            formatted.append(f"{safe_var}={safe_value}")

        result = ", ".join(formatted)
        return result[:100] + "..." if len(result) > 100 else result

    def _trim_explanation(self, explanation: str) -> str:
        """Trim explanation to ensure brevity"""
        if not explanation:
            return "Execute step"

        # Remove verbose prefixes
        prefixes_to_remove = [
            "The algorithm", "In this step", "This operation", "The hash map",
            "The two pointers", "We are", "This step", "Now we"
        ]

        cleaned = explanation.strip()
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                if cleaned.startswith(','):
                    cleaned = cleaned[1:].strip()

        # Take first sentence and limit words
        sentences = re.split(r'[.!?]', cleaned)
        if sentences:
            first_sentence = sentences[0].strip()
            words = first_sentence.split()[:15]  # Max 15 words
            result = ' '.join(words)

            # Ensure proper capitalization
            if result and not result[0].isupper():
                result = result[0].upper() + result[1:]

            return result

        return cleaned[:100] if cleaned else "Execute step"

    def _generate_visualization_data(
            self,
            step: ExecutionStep,
            pattern: AlgorithmPattern
    ) -> Dict[str, Any]:
        """Generate visualization data for step"""
        viz_data = {
            "step_type": getattr(step, 'event_type', 'execution'),
            "data_structure_state": {},
            "pointers": {},
            "highlights": [],
            "annotations": {}
        }

        variables_after = getattr(step, 'variables_after', step.variable_changes)

        # Extract data structures
        for var_name, var_value in variables_after.items():
            if isinstance(var_value, (list, tuple)):
                viz_data["data_structure_state"][var_name] = {
                    "type": "array",
                    "values": list(var_value)
                }
            elif isinstance(var_value, dict):
                viz_data["data_structure_state"][var_name] = {
                    "type": "hash_map",
                    "entries": dict(var_value)
                }

        # Extract pointers
        pointer_vars = ['left', 'right', 'start', 'end', 'low', 'high', 'mid', 'i', 'j']
        for var in pointer_vars:
            if var in variables_after:
                viz_data["pointers"][var] = variables_after[var]

        # Extract highlights based on variable changes
        for var_name in step.variable_changes.keys():
            if var_name in pointer_vars and var_name in variables_after:
                viz_data["highlights"].append(variables_after[var_name])

        return viz_data


class FallbackStepExplainer:
    """Rule-based step explainer as fallback when Ollama is not available"""

    def explain_step(
            self,
            code_line: str,
            variables_before: Dict[str, Any],
            variables_after: Dict[str, Any],
            algorithm_pattern: AlgorithmPattern
    ) -> str:
        """Generate explanation for a single execution step"""
        code_line = code_line.strip().lower()

        # Check what operation is happening
        if 'complement' in code_line:
            return self._explain_complement_check(variables_before, variables_after)
        elif 'nummap' in code_line or 'map' in code_line:
            return self._explain_hashmap_operation(code_line, variables_before, variables_after)
        elif 'left' in code_line and 'right' in code_line:
            return self._explain_two_pointers(code_line, variables_before, variables_after)
        elif 'return' in code_line:
            return self._explain_return_statement(variables_after)
        else:
            return f"Execute: {code_line[:50]}..."

    def _explain_complement_check(
            self,
            variables_before: Dict[str, Any],
            variables_after: Dict[str, Any]
    ) -> str:
        """Explain complement checking operation"""
        complement = variables_after.get('complement')
        if complement is not None:
            return f"Calculate complement: target - current = {complement}"
        return "Check if complement exists in hash map"

    def _explain_hashmap_operation(
            self,
            code_line: str,
            variables_before: Dict[str, Any],
            variables_after: Dict[str, Any]
    ) -> str:
        """Explain hash map operations"""
        if '=' in code_line and 'map' in code_line:
            return "Store value and its index in hash map for O(1) lookup"
        elif 'in' in code_line and 'map' in code_line:
            return "Check if complement exists in hash map (O(1) operation)"
        return "Hash map operation"

    def _explain_two_pointers(
            self,
            code_line: str,
            variables_before: Dict[str, Any],
            variables_after: Dict[str, Any]
    ) -> str:
        """Explain two pointers operations"""
        left = variables_after.get('left', variables_before.get('left'))
        right = variables_after.get('right', variables_before.get('right'))

        if 'left' in code_line and '+' in code_line:
            return f"Move left pointer forward: left = {left}"
        elif 'right' in code_line and '-' in code_line:
            return f"Move right pointer backward: right = {right}"
        elif '<' in code_line or '>' in code_line:
            return f"Check if pointers haven't crossed: {left} vs {right}"
        return f"Two pointers operation: left={left}, right={right}"

    def _explain_return_statement(self, variables_after: Dict[str, Any]) -> str:
        """Explain return statements"""
        return "Return solution from function"


# Factory function to get appropriate explainer
def get_step_explainer(llm_model: str = None) -> StepExplainer:
    """Factory function to get appropriate step explainer with optional model"""
    try:
        if llm_model:
            # Create StepExplainer with specific model
            return StepExplainer(model_name=llm_model)
        else:
            # Create StepExplainer with default model
            return StepExplainer()
    except Exception as e:
        logger.warning(f"Failed to initialize StepExplainer with model {llm_model}: {e}")
        # Return a minimal explainer that uses only fallback
        class MinimalExplainer:
            def __init__(self):
                self.fallback = FallbackStepExplainer()

            def enhance_steps_with_explanations(self, steps, pattern, context):
                enhanced_steps = []
                for step in steps:
                    # Create enhanced step with fallback explanation
                    enhanced_step = ExecutionStep(
                        step_number=step.step_number,
                        code_line=step.code_line,
                        variable_changes=step.variable_changes,
                        variables_before=getattr(step, 'variables_before', {}),
                        variables_after=getattr(step, 'variables_after', {}),
                        event_type=getattr(step, 'event_type', 'execution'),
                        explanation="",
                        visualization_data={}
                    )

                    enhanced_step.explanation = self.fallback.explain_step(
                        step.code_line,
                        getattr(step, 'variables_before', {}),
                        getattr(step, 'variables_after', {}),
                        pattern
                    )

                    # Generate basic visualization data
                    enhanced_step.visualization_data = {
                        "step_type": "execution",
                        "data_structure_state": {},
                        "pointers": {},
                        "highlights": []
                    }

                    enhanced_steps.append(enhanced_step)

                return enhanced_steps

        return MinimalExplainer()
