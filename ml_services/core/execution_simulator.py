# ml_services/core/execution_simulator.py - UPDATED VERSION
from typing import Dict, Any, List, Optional
from core.safe_executor import SafeExecutor
from core.step_explainer import get_step_explainer
from core.execution_tracker import ExecutionStep
from models.internal_models import ProcessedInput, AlgorithmPattern
from config.log_config import get_logger

logger = get_logger(__name__)

class ExecutionSimulator:
    """Phase 3 + Phase 4: Code execution simulation with AI-enhanced step explanations"""

    def __init__(self, llm_model: str = "codellama:7b-instruct"):
        self.safe_executor = SafeExecutor(timeout_seconds=10, memory_limit_mb=100)
        self.step_explainer = get_step_explainer(llm_model)  # AI-enhanced explainer with fallback

    def simulate_execution(self,
                           processed_input: ProcessedInput,
                           algorithm_pattern: AlgorithmPattern) -> Dict[str, Any]:
        """
        Main Phase 3 + Phase 4 entry point: Execute code and generate AI-enhanced educational steps

        Args:
            processed_input: Output from Phase 1 (validation) and Phase 2 (pattern detection)
            algorithm_pattern: Detected algorithm pattern from Phase 2

        Returns:
            Dict containing execution steps with AI explanations and visualization data
        """

        logger.info(f"Starting Phase 3+4 execution simulation for pattern: {algorithm_pattern}")

        if not processed_input.selected_test_case:
            raise ValueError("No test case selected for execution")

        try:
            # Phase 3: Execute code with tracing
            raw_steps = self._execute_and_trace(processed_input)

            if not raw_steps:
                logger.warning("No execution steps captured - code may not have executed properly")
                return self._create_empty_result(algorithm_pattern)

            # Phase 4: Enhance steps with AI explanations
            enhanced_steps = self._enhance_with_ai(raw_steps, algorithm_pattern, processed_input)

            # Generate execution summary
            execution_summary = self._generate_execution_summary(enhanced_steps, algorithm_pattern)

            logger.info(f"Phase 3+4 completed: Generated {len(enhanced_steps)} AI-enhanced steps")

            return {
                'execution_steps': [self._step_to_dict(step) for step in enhanced_steps],
                'execution_summary': execution_summary,
                'total_steps': len(enhanced_steps),
                'algorithm_pattern': algorithm_pattern.value,
                'ai_enhanced': True,  # Flag indicating AI enhancement
                'test_case_used': {
                    'input': processed_input.selected_test_case.input_data,
                    'expected_output': processed_input.selected_test_case.expected_output
                }
            }

        except Exception as e:
            logger.error(f"Phase 3+4 execution failed: {e}")
            return {
                'error': str(e),
                'execution_steps': [],
                'total_steps': 0,
                'ai_enhanced': False
            }

    def _execute_and_trace(self, processed_input: ProcessedInput) -> List[ExecutionStep]:
        """Phase 3: Execute code with tracing"""
        test_inputs = processed_input.selected_test_case.input_data
        main_function = self._extract_main_function_name(processed_input.code_ast)

        logger.info(f"Executing code with function: {main_function}")

        try:
            # Try SafeExecutor first
            safe_executor = SafeExecutor(timeout_seconds=10, memory_limit_mb=100)
            raw_steps = safe_executor.execute_with_tracing(
                code=processed_input.cleaned_code,
                inputs=test_inputs,
                function_name=main_function
            )
            logger.info(f"Captured {len(raw_steps)} raw execution steps")
            return raw_steps
            
        except Exception as e:
            logger.warning(f"SafeExecutor failed: {e}, using simple executor")
            
            # Fallback to SimpleExecutor
            from core.simple_executor import SimpleExecutor
            simple_executor = SimpleExecutor()
            raw_steps = simple_executor.execute_with_tracing(
                code=processed_input.cleaned_code,
                inputs=test_inputs,
                function_name=main_function
            )
            logger.info(f"Simple executor generated {len(raw_steps)} steps")
            return raw_steps

    def _enhance_with_ai(self,
                         steps: List[ExecutionStep],
                         pattern: AlgorithmPattern,
                         processed_input: ProcessedInput) -> List[ExecutionStep]:
        """Phase 4: Enhance steps with AI explanations"""

        problem_context = {
            'problem_description': processed_input.problem_data.description if processed_input.problem_data else 'Algorithm execution',
            'expected_output': processed_input.selected_test_case.expected_output,
            'test_input': processed_input.selected_test_case.input_data,
            'algorithm_pattern': pattern.value
        }

        logger.info("Enhancing steps with AI explanations...")

        enhanced_steps = self.step_explainer.enhance_steps_with_explanations(
            steps=steps,
            algorithm_pattern=pattern,
            problem_context=problem_context
        )

        return enhanced_steps

    def _extract_main_function_name(self, code_ast) -> Optional[str]:
        """Extract the main function name from AST"""
        if not code_ast:
            return None

        import ast
        for node in ast.walk(code_ast):
            if isinstance(node, ast.FunctionDef):
                return node.name

        return None

    def _step_to_dict(self, step: ExecutionStep) -> Dict[str, Any]:
        """Convert ExecutionStep to dictionary for JSON serialization"""
        return {
            'step_number': step.step_number,
            'line_number': step.line_number,
            'code_line': step.code_line,
            'function_name': step.function_name,
            'event_type': step.event_type,
            'explanation': step.explanation,  # AI-enhanced explanation
            'variable_changes': step.variable_changes,
            'visualization_data': step.visualization_data,
            'is_significant': step.is_significant,
            'ai_generated': True  # Flag for AI-generated explanations
        }

    def _generate_execution_summary(self, steps: List[ExecutionStep], pattern: AlgorithmPattern) -> Dict[str, Any]:
        """Generate comprehensive summary of AI-enhanced execution"""
        significant_steps = [s for s in steps if s.is_significant]

        # Count different types of operations
        operation_counts = {
            'variable_assignments': 0,
            'function_calls': 0,
            'control_flow': 0,
            'data_operations': 0
        }

        for step in steps:
            if step.variable_changes:
                operation_counts['variable_assignments'] += 1
            if step.event_type == 'call':
                operation_counts['function_calls'] += 1
            if any(keyword in step.code_line.lower() for keyword in ['if', 'while', 'for', 'else']):
                operation_counts['control_flow'] += 1
            if any(keyword in step.code_line.lower() for keyword in ['append', 'pop', 'insert', 'remove']):
                operation_counts['data_operations'] += 1

        return {
            'total_lines_executed': len(steps),
            'significant_steps': len(significant_steps),
            'algorithm_pattern': pattern.value,
            'operation_counts': operation_counts,
            'key_operations': self._identify_key_operations(steps, pattern),
            'performance_notes': self._generate_performance_notes(steps, pattern),
            'ai_enhanced': True,
            'complexity_analysis': self._get_complexity_analysis(pattern)
        }

    def _identify_key_operations(self, steps: List[ExecutionStep], pattern: AlgorithmPattern) -> List[str]:
        """Identify key algorithmic operations from execution"""
        operations = []

        for step in steps:
            code = step.code_line.lower()

            if pattern == AlgorithmPattern.HASH_MAP:
                if 'in ' in code:
                    operations.append('Hash table lookup')
                elif '[' in code and '=' in code:
                    operations.append('Hash table insertion')
            elif pattern == AlgorithmPattern.TWO_POINTERS:
                if any(var in step.variable_changes for var in ['left', 'right', 'start', 'end']):
                    operations.append('Pointer movement')
            elif pattern == AlgorithmPattern.SLIDING_WINDOW:
                if 'while' in code or 'for' in code:
                    operations.append('Window adjustment')
            elif pattern == AlgorithmPattern.BINARY_SEARCH:
                if 'mid' in step.variable_changes:
                    operations.append('Search space division')

        return list(set(operations))  # Remove duplicates

    def _generate_performance_notes(self, steps: List[ExecutionStep], pattern: AlgorithmPattern) -> List[str]:
        """Generate AI-aware performance notes"""
        notes = []

        if pattern == AlgorithmPattern.HASH_MAP:
            notes.append("Hash table operations provide O(1) average lookup time")
            notes.append("Space complexity is O(n) for storing key-value pairs")
        elif pattern == AlgorithmPattern.TWO_POINTERS:
            notes.append("Two pointers technique reduces time complexity to O(n)")
            notes.append("Space complexity is O(1) - only using pointer variables")
        elif pattern == AlgorithmPattern.SLIDING_WINDOW:
            notes.append("Sliding window avoids nested loops, maintaining O(n) complexity")
            notes.append("Efficient for subarray/substring problems")
        elif pattern == AlgorithmPattern.BINARY_SEARCH:
            notes.append("Binary search achieves O(log n) by halving search space each iteration")
            notes.append("Requires sorted input data for correctness")

        return notes

    def _get_complexity_analysis(self, pattern: AlgorithmPattern) -> Dict[str, str]:
        """Get complexity analysis for the algorithm pattern"""
        complexity_map = {
            AlgorithmPattern.HASH_MAP: {"time": "O(n)", "space": "O(n)"},
            AlgorithmPattern.TWO_POINTERS: {"time": "O(n)", "space": "O(1)"},
            AlgorithmPattern.SLIDING_WINDOW: {"time": "O(n)", "space": "O(1)"},
            AlgorithmPattern.BINARY_SEARCH: {"time": "O(log n)", "space": "O(1)"}
        }

        return complexity_map.get(pattern, {"time": "O(?)", "space": "O(?)"})

    def _create_empty_result(self, pattern: AlgorithmPattern) -> Dict[str, Any]:
        """Create empty result when execution fails"""
        return {
            'execution_steps': [],
            'execution_summary': {
                'total_lines_executed': 0,
                'significant_steps': 0,
                'algorithm_pattern': pattern.value,
                'ai_enhanced': False
            },
            'total_steps': 0,
            'algorithm_pattern': pattern.value,
            'ai_enhanced': False,
            'error': 'No execution steps captured'
        }
