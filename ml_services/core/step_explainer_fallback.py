# Fallback step explainer when Ollama is not available
from typing import List, Dict, Any
from core.execution_tracker import ExecutionStep
from models.internal_models import AlgorithmPattern
from config.log_config import get_logger

logger = get_logger(__name__)

class FallbackStepExplainer:
    """Fallback step explainer without AI dependencies"""

    def __init__(self):
        self.explanation_cache = {}

    def enhance_steps_with_explanations(self, steps: List[ExecutionStep], algorithm_pattern: AlgorithmPattern, problem_context: Dict[str, Any]) -> List[ExecutionStep]:
        """Add basic explanations to execution steps"""
        enhanced_steps = []

        for step in steps:
            step.explanation = self._generate_fallback_explanation(step, algorithm_pattern)
            step.visualization_data = self._generate_visualization_data(step, algorithm_pattern)
            enhanced_steps.append(step)

        logger.info(f"Enhanced {len(enhanced_steps)} steps with fallback explanations")
        return enhanced_steps

    def _generate_fallback_explanation(self, step: ExecutionStep, pattern: AlgorithmPattern) -> str:
        """Generate basic explanation without AI"""
        code_line = step.code_line.strip()

        if pattern == AlgorithmPattern.HASH_MAP:
            if 'in ' in code_line:
                return "Check if complement exists in hash map."
            elif '[' in code_line and '=' in code_line:
                return "Store number-index pair for lookup."
            elif '{}' in code_line:
                return "Initialize empty hash map."

        elif pattern == AlgorithmPattern.TWO_POINTERS:
            if 'left' in step.variable_changes:
                return "Move left pointer right."
            elif 'right' in step.variable_changes:
                return "Move right pointer left."

        elif pattern == AlgorithmPattern.BINARY_SEARCH:
            if 'mid' in step.variable_changes:
                return "Calculate middle index."
            elif 'left' in step.variable_changes:
                return "Search right half."
            elif 'right' in step.variable_changes:
                return "Search left half."

        # Generic fallback
        if step.variable_changes:
            changes = list(step.variable_changes.keys())[:2]
            return f"Update {', '.join(changes)}."
        
        return f"Execute: {code_line[:30]}..."

    def _generate_visualization_data(self, step: ExecutionStep, pattern: AlgorithmPattern) -> Dict[str, Any]:
        """Generate visualization data for frontend"""
        viz_data = {
            'step_type': step.event_type,
            'highlights': [],
            'data_structure_state': {},
            'pointers': {},
            'progress': {}
        }

        # Extract data structures from variables
        for var_name, var_value in step.variables_after.items():
            if isinstance(var_value, (list, tuple)):
                viz_data['data_structure_state'][var_name] = {
                    'type': 'array',
                    'values': list(var_value),
                    'length': len(var_value)
                }
            elif isinstance(var_value, dict):
                viz_data['data_structure_state'][var_name] = {
                    'type': 'hash_map',
                    'entries': dict(var_value),
                    'size': len(var_value)
                }

        # Add pointer information
        pointer_vars = ['left', 'right', 'start', 'end', 'low', 'high', 'mid', 'i', 'j']
        for var in pointer_vars:
            if var in step.variables_after:
                viz_data['pointers'][var] = step.variables_after[var]

        # Highlight changed variables
        for var_name in step.variable_changes:
            viz_data['highlights'].append(var_name)

        return viz_data