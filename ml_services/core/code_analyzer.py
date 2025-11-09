import ast
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from models.internal_models import ProcessedInput, AlgorithmPattern, ProblemType
from config.log_config import get_logger
from core.ai_pattern_matcher import AIPatternMatcher
from core.execution_simulator import ExecutionSimulator

logger = get_logger(__name__)

class DataStructureType(str, Enum):
    ARRAY = "array"
    HASH_MAP = "hash_map"
    SET = "set"
    STACK = "stack"
    QUEUE = "queue"
    TREE = "tree"
    GRAPH = "graph"
    STRING = "string"

@dataclass
class CodeStructure:
    """Represents the analyzed structure of the code"""
    functions: List[Dict[str, Any]]
    variables: Dict[str, str]  # name -> type
    data_structures: List[DataStructureType]
    control_flow: List[str]  # loops, conditionals
    complexity_indicators: Dict[str, str]
    return_pattern: Optional[str]
    code_text: str = ""  # Add code text for AI matcher

@dataclass
class AlgorithmAnalysis:
    """Complete algorithm analysis result"""
    primary_pattern: Optional[AlgorithmPattern]
    confidence_score: float
    problem_alignment: float  # How well code matches problem
    data_structures_used: List[DataStructureType]
    time_complexity: str
    space_complexity: str
    optimization_techniques: List[str]
    potential_issues: List[str]
    # Phase 3 fields
    execution_steps: List[Dict[str, Any]] = field(default_factory=list)
    execution_summary: Dict[str, Any] = field(default_factory=dict)

class CodeAnalyzer:
    """Phase 2: Code Understanding & Pattern Recognition with AI + Phase 3: Execution Simulation"""

    def __init__(self):
        # Keep rule-based matchers as fallback
        from core.pattern_matchers import PatternMatchers
        self.rule_based_matchers = PatternMatchers()

        self.pattern_matchers = {
            AlgorithmPattern.HASH_MAP: self.rule_based_matchers._match_hash_map_pattern,
            AlgorithmPattern.TWO_POINTERS: self.rule_based_matchers._match_two_pointers_pattern,
            AlgorithmPattern.SLIDING_WINDOW: self.rule_based_matchers._match_sliding_window_pattern,
            AlgorithmPattern.BINARY_SEARCH: self.rule_based_matchers._match_binary_search_pattern,
            AlgorithmPattern.DEPTH_FIRST_SEARCH: self.rule_based_matchers._match_dfs_pattern,
            AlgorithmPattern.DYNAMIC_PROGRAMMING: self.rule_based_matchers._match_dp_pattern,
            AlgorithmPattern.GREEDY: self.rule_based_matchers._match_greedy_pattern,
        }

        # Add AI-powered matcher
        self.ai_matcher = AIPatternMatcher()

        # Train if not already trained
        if not self.ai_matcher.is_trained:
            self._train_ai_matcher()

        # Algorithm pattern templates for matching
        self.algorithm_templates = self._initialize_algorithm_templates()

        # Phase 3: Add execution simulator
        self.execution_simulator = ExecutionSimulator()

    def _train_ai_matcher(self):
        """Train the AI matcher with sample data"""
        try:
            from data.training_data_builder import TrainingDataBuilder

            logger.info("Training AI pattern matcher...")
            builder = TrainingDataBuilder()
            training_data = builder.add_samples()

            if training_data:
                metrics = self.ai_matcher.train(training_data)
                logger.info(f"AI training completed: {metrics}")
            else:
                logger.warning("No training data available")
        except Exception as e:
            logger.warning(f"AI training failed: {e}. Will use rule-based fallback.")

    def analyze(self, processed_input: ProcessedInput) -> Optional[AlgorithmAnalysis]:
        """Main analysis entry point - orchestrates Phase 2 & Phase 3 steps"""
        logger.info("Starting Phase 2: Code Understanding & Pattern Recognition")

        if processed_input.code_ast is None:
            logger.warning("No AST available for analysis")
            return None

        try:
            # Step 2.1: Enhanced AST Analysis
            code_structure = self._analyze_code_structure(processed_input.code_ast, processed_input.cleaned_code)

            # Step 2.2: Algorithm Pattern Matching (AI + Rule-based)
            pattern_results = self._match_algorithm_patterns(
                processed_input.code_ast,
                code_structure,
                processed_input.problem_data
            )

            # Step 2.3: Problem-Code Alignment Verification
            alignment_score = self._verify_problem_alignment(
                code_structure,
                processed_input.problem_data,
                pattern_results
            )

            # Combine results into comprehensive analysis
            analysis = AlgorithmAnalysis(
                primary_pattern=pattern_results.get('primary_pattern'),
                confidence_score=pattern_results.get('confidence', 0.0),
                problem_alignment=alignment_score,
                data_structures_used=code_structure.data_structures,
                time_complexity=self._estimate_time_complexity(code_structure),
                space_complexity=self._estimate_space_complexity(code_structure),
                optimization_techniques=self._identify_optimizations(code_structure),
                potential_issues=self._identify_potential_issues(code_structure, processed_input.problem_data)
            )

            logger.info(f"Analysis complete. Pattern: {analysis.primary_pattern}, Confidence: {analysis.confidence_score:.2f}")

            # Phase 3: Execute and generate steps (NEW)
            if analysis.primary_pattern and processed_input.selected_test_case:
                try:
                    logger.info("Starting Phase 3: Execution Simulation")
                    execution_results = self.execution_simulator.simulate_execution(
                        processed_input=processed_input,
                        algorithm_pattern=analysis.primary_pattern
                    )

                    # Store execution results
                    analysis.execution_steps = execution_results.get('execution_steps', [])
                    analysis.execution_summary = execution_results.get('execution_summary', {})

                    logger.info(f"Phase 3 completed: Generated {len(analysis.execution_steps)} execution steps")

                except Exception as e:
                    logger.error(f"Phase 3 failed, continuing with Phase 2 results: {e}")
                    # Phase 3 failure doesn't break the system - Phase 2 results are still valuable
            else:
                logger.info("Skipping Phase 3: No pattern detected or no test case available")

            return analysis

        except Exception as e:
            logger.error(f"Error during code analysis: {e}", exc_info=True)
            return None

    def _analyze_code_structure(self, tree: ast.AST, code_text: str = "") -> CodeStructure:
        """Step 2.1: Enhanced AST Analysis"""
        functions = []
        variables = {}
        data_structures = []
        control_flow = []
        complexity_indicators = {}
        return_pattern = None

        for node in ast.walk(tree):
            # Analyze functions
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'return_statements': len([n for n in ast.walk(node) if isinstance(n, ast.Return)]),
                    'nested_loops': self._count_nested_loops(node),
                    'recursion': self._has_recursion(node)
                }
                functions.append(func_info)

            # Analyze variable assignments and data structure creation
            elif isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Dict):
                    data_structures.append(DataStructureType.HASH_MAP)
                elif isinstance(node.value, ast.List):
                    data_structures.append(DataStructureType.ARRAY)
                elif isinstance(node.value, ast.Set):
                    data_structures.append(DataStructureType.SET)

                # Track variable types
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables[target.id] = self._infer_type(node.value)

            # Analyze control flow
            elif isinstance(node, (ast.For, ast.While)):
                control_flow.append(f"loop_{node.__class__.__name__.lower()}")
                if self._is_nested_loop(node):
                    complexity_indicators['nested_loops'] = 'O(n²) or higher'

            elif isinstance(node, ast.If):
                control_flow.append("conditional")

            # Analyze return patterns
            elif isinstance(node, ast.Return):
                return_pattern = self._analyze_return_pattern(node)

        return CodeStructure(
            functions=functions,
            variables=variables,
            data_structures=list(set(data_structures)),  # Remove duplicates
            control_flow=control_flow,
            complexity_indicators=complexity_indicators,
            return_pattern=return_pattern,
            code_text=code_text
        )

    def _match_algorithm_patterns(self, tree: ast.AST, structure: CodeStructure, problem_data) -> Dict[str, Any]:
        """Step 2.2: Enhanced Algorithm Pattern Matching - AI first, rule-based fallback"""

        # Try AI first
        try:
            ai_pattern, ai_confidence = self.ai_matcher.predict_pattern(tree, structure.code_text)

            if ai_pattern and ai_confidence >= 0.7:  # High confidence threshold
                logger.info(f"AI detected pattern: {ai_pattern} (confidence: {ai_confidence:.3f})")
                return {
                    'primary_pattern': ai_pattern,
                    'confidence': ai_confidence,
                    'method': 'ai'
                }
        except Exception as e:
            logger.warning(f"AI pattern matching failed: {e}")

        # Fallback to rule-based
        logger.info("Using rule-based pattern matching as fallback")
        pattern_scores = {}

        for pattern, matcher in self.pattern_matchers.items():
            try:
                score = matcher(tree, structure, problem_data)
                if score > 0:
                    pattern_scores[pattern] = score
            except Exception as e:
                logger.warning(f"Rule-based matcher {pattern} failed: {e}")

        if pattern_scores:
            best_pattern = max(pattern_scores, key=pattern_scores.get)
            confidence = pattern_scores[best_pattern]
            return {
                'primary_pattern': best_pattern,
                'confidence': min(confidence, 1.0),
                'method': 'rule_based'
            }

        return {'primary_pattern': None, 'confidence': 0.0, 'method': 'none'}

    def _verify_problem_alignment(self, structure: CodeStructure, problem_data, pattern_results) -> float:
        """Step 2.3: Problem-Code Alignment Verification"""
        alignment_factors = []

        # Check if data structures match problem type
        problem_type = problem_data.problem_type
        if problem_type == ProblemType.ARRAY and DataStructureType.ARRAY in structure.data_structures:
            alignment_factors.append(0.3)
        elif problem_type == ProblemType.STRING and DataStructureType.STRING in structure.data_structures:
            alignment_factors.append(0.3)

        # Check if algorithm pattern matches problem hints
        if pattern_results.get('primary_pattern'):
            # Hash map patterns often work well for lookup problems
            if 'lookup' in problem_data.description.lower() and pattern_results['primary_pattern'] == AlgorithmPattern.HASH_MAP:
                alignment_factors.append(0.4)

        # Check constraint compliance
        constraints_met = self._check_constraint_compliance(structure, problem_data.constraints)
        if constraints_met:
            alignment_factors.append(0.3)

        return sum(alignment_factors) if alignment_factors else 0.0

    def _match_hash_map_pattern(self, tree: ast.AST, structure: CodeStructure, problem_data) -> float:
        """Legacy method - now delegates to PatternMatchers"""
        return self.rule_based_matchers._match_hash_map_pattern(tree, structure, problem_data)

    # Helper methods for analysis (existing methods unchanged)
    def _count_nested_loops(self, node: ast.AST) -> int:
        """Count maximum nesting depth of loops"""
        class LoopDepthVisitor(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0

            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

        visitor = LoopDepthVisitor()
        visitor.visit(node)
        return visitor.max_depth

    def _has_recursion(self, func_node: ast.FunctionDef) -> bool:
        """Check if function calls itself"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == func_node.name:
                    return True
        return False

    def _infer_type(self, value_node: ast.AST) -> str:
        """Infer variable type from assignment"""
        if isinstance(value_node, ast.Dict):
            return "dict"
        elif isinstance(value_node, ast.List):
            return "list"
        elif isinstance(value_node, ast.Set):
            return "set"
        elif isinstance(value_node, ast.Constant):
            return type(value_node.value).__name__
        else:
            return "unknown"

    def _is_nested_loop(self, loop_node: ast.AST) -> bool:
        """Check if this loop is nested inside another loop"""
        nested_loops = [node for node in ast.walk(loop_node) if isinstance(node, (ast.For, ast.While)) and node != loop_node]
        return len(nested_loops) > 0

    def _analyze_return_pattern(self, return_node: ast.Return) -> str:
        """Analyze the pattern of return statements"""
        if return_node.value is None:
            return "void"
        elif isinstance(return_node.value, ast.List):
            return "list"
        elif isinstance(return_node.value, ast.Constant):
            return "constant"
        else:
            return "expression"

    def _estimate_time_complexity(self, structure: CodeStructure) -> str:
        """Estimate time complexity based on code structure"""
        if structure.complexity_indicators.get('nested_loops'):
            return "O(n²)"
        elif 'loop_for' in structure.control_flow or 'loop_while' in structure.control_flow:
            return "O(n)"
        else:
            return "O(1)"

    def _estimate_space_complexity(self, structure: CodeStructure) -> str:
        """Estimate space complexity based on data structures"""
        if DataStructureType.HASH_MAP in structure.data_structures:
            return "O(n)"
        elif DataStructureType.ARRAY in structure.data_structures:
            return "O(n)"
        else:
            return "O(1)"

    def _identify_optimizations(self, structure: CodeStructure) -> List[str]:
        """Identify optimization techniques used"""
        optimizations = []
        if DataStructureType.HASH_MAP in structure.data_structures:
            optimizations.append("Hash table lookup for O(1) access")
        if structure.complexity_indicators.get('nested_loops'):
            optimizations.append("Could potentially be optimized to reduce nested loops")
        return optimizations

    def _identify_potential_issues(self, structure: CodeStructure, problem_data) -> List[str]:
        """Identify potential issues with the algorithm"""
        issues = []
        if structure.complexity_indicators.get('nested_loops') and 'linear' in problem_data.description.lower():
            issues.append("Nested loops may violate linear time complexity requirement")
        if not structure.functions:
            issues.append("No function definition found")
        return issues

    def _check_constraint_compliance(self, structure: CodeStructure, constraints) -> bool:
        """Check if algorithm structure complies with problem constraints"""
        for constraint in constraints:
            if constraint.type == "time_complexity":
                if "linear" in constraint.value.lower() and structure.complexity_indicators.get('nested_loops'):
                    return False
        return True

    def _initialize_algorithm_templates(self) -> Dict[str, Dict]:
        """Initialize algorithm pattern templates for matching"""
        return {
            'two_sum_hash': {
                'data_structures': [DataStructureType.HASH_MAP],
                'pattern': 'single_loop_with_lookup',
                'keywords': ['complement', 'target', 'difference']
            },
            'binary_search': {
                'data_structures': [DataStructureType.ARRAY],
                'pattern': 'divide_and_conquer',
                'keywords': ['mid', 'left', 'right', 'sorted']
            }
        }
