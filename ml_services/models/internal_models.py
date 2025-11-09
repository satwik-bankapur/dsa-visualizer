from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
import ast

class Language(str, Enum):
    PYTHON = "python"
    UNKNOWN = "unknown"

class ProblemType(str, Enum):
    ARRAY = "array"
    STRING = "string"
    TREE = "tree"
    GRAPH = "graph"
    HASH_TABLE = "hash_table"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    SLIDING_WINDOW = "sliding_window"
    TWO_POINTERS = "two_pointers"

class AlgorithmPattern(str, Enum):
    HASH_MAP = "hash_map"
    TWO_POINTERS = "two_pointers"
    SLIDING_WINDOW = "sliding_window"
    BINARY_SEARCH = "binary_search"
    DEPTH_FIRST_SEARCH = "depth_first_search"
    BREADTH_FIRST_SEARCH = "bfs"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    GREEDY = "greedy"
    BACKTRACKING = "backtracking"
    DIVIDE_AND_CONQUER = "divide_and_conquer"

class OptimizationTechnique(str, Enum):
    MEMOIZATION = "memoization"
    EARLY_TERMINATION = "early_termination"
    SPACE_TIME_TRADEOFF = "space_time_tradeoff"
    IN_PLACE_MODIFICATION = "in_place_modification"
    PREPROCESSING = "preprocessing"

class DataStructureType(str, Enum):
    ARRAY = "array"
    HASH_MAP = "hash_map"
    SET = "set"
    STACK = "stack"
    QUEUE = "queue"
    TREE = "tree"
    GRAPH = "graph"
    STRING = "string"
    LINKED_LIST = "linked_list"

class Constraint(BaseModel):
    type: str
    value: str

class TestCase(BaseModel):
    input_data: Dict[str, Any]
    expected_output: Any

class ProblemData(BaseModel):
    title: str
    description: str
    constraints: List[Constraint] = []
    test_cases: List[TestCase] = []
    problem_type: Optional[ProblemType] = None

class CodeMetadata(BaseModel):
    language: Language
    function_name: Optional[str] = None
    parameters: List[str] = []
    lines_of_code: int = 0
    cyclomatic_complexity: int = 1

class CodeStructureAnalysis(BaseModel):
    """Enhanced code structure analysis from Phase 2"""
    functions: List[Dict[str, Any]] = []
    variables: Dict[str, str] = {}
    data_structures_used: List[DataStructureType] = []
    control_flow_patterns: List[str] = []
    nested_loop_depth: int = 0
    has_recursion: bool = False
    return_pattern: Optional[str] = None
    time_complexity_estimate: str = "O(1)"
    space_complexity_estimate: str = "O(1)"

class AlgorithmAnalysis(BaseModel):
    """Complete algorithm analysis result from Phase 2"""
    primary_pattern: Optional[AlgorithmPattern] = None
    confidence_score: float = 0.0
    problem_alignment_score: float = 0.0
    data_structures_used: List[DataStructureType] = []
    time_complexity: str = "O(1)"
    space_complexity: str = "O(1)"
    optimization_techniques: List[OptimizationTechnique] = []
    potential_issues: List[str] = []
    algorithm_completeness: float = 0.0  # How complete the implementation is
    edge_case_handling: List[str] = []  # Edge cases the code handles
    execution_steps: List[Dict[str, Any]] = Field(default_factory=list)
    execution_summary: Dict[str, Any] = Field(default_factory=dict)

class ProcessedInput(BaseModel):
    original_code: str
    cleaned_code: str
    problem_data: ProblemData
    code_metadata: CodeMetadata
    selected_test_case: Optional[TestCase] = None
    validation_errors: List[str] = []
    code_ast: Optional[ast.AST] = None

    # Enhanced Phase 2 analysis results
    code_structure: Optional[CodeStructureAnalysis] = None
    algorithm_analysis: Optional[AlgorithmAnalysis] = None

    class Config:
        arbitrary_types_allowed = True

# Additional models for Phase 2 enhancements
class PatternMatchingResult(BaseModel):
    """Result of pattern matching analysis"""
    pattern: AlgorithmPattern
    confidence: float
    evidence: List[str]  # What evidence supports this pattern
    missing_components: List[str]  # What's missing for this pattern

class ComplexityAnalysis(BaseModel):
    """Detailed complexity analysis"""
    time_complexity: str
    space_complexity: str
    best_case: str
    worst_case: str
    average_case: str
    complexity_justification: str

class CodeQualityMetrics(BaseModel):
    """Code quality and correctness metrics"""
    readability_score: float
    efficiency_score: float
    correctness_probability: float
    maintainability_score: float
    test_coverage_estimate: float