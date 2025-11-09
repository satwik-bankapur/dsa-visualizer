# ml_services/schemas/analysis_schemas.py - Enhanced with Phase 2 Response Models
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from models.internal_models import Language, AlgorithmPattern, ProblemType, DataStructureType

class TestCaseInput(BaseModel):
    input_data: Dict[str, Any] = Field(..., description="Input parameters for the test case")
    expected_output: Any = Field(..., description="Expected output for the test case")

class CodeAnalysisRequest(BaseModel):
    code_string: str = Field(..., min_length=10, description="The code to analyze")
    problem_statement: str = Field(..., min_length=20, description="The problem description")
    language: Language = Field(default=Language.PYTHON, description="Programming language")
    test_cases: Optional[List[TestCaseInput]] = Field(default=[], description="Optional test cases")

    @validator("code_string", "problem_statement")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

# Phase 2 Response Models
class ProblemAnalysisResponse(BaseModel):
    problem_type: Optional[str] = Field(description="Detected problem type")
    title: str = Field(description="Problem title")
    constraints_count: int = Field(description="Number of constraints found")
    test_cases_count: int = Field(description="Number of test cases provided")

class CodeMetadataResponse(BaseModel):
    detected_language: str = Field(description="Programming language detected")
    function_name: Optional[str] = Field(description="Main function name")
    parameters: List[str] = Field(description="Function parameters")
    lines_of_code: int = Field(description="Total lines of code")

class ExecutionStepResponse(BaseModel):
    step_number: int = Field(description="Step sequence number")
    code_line: str = Field(description="Code line being executed")
    explanation: str = Field(description="Educational explanation of this step")
    variable_changes: Dict[str, Any] = Field(description="Variables that changed")
    visualization_data: Dict[str, Any] = Field(description="Data for frontend visualization")

class AlgorithmAnalysisResponse(BaseModel):
    primary_pattern: Optional[str] = Field(description="Primary algorithm pattern detected")
    confidence_score: float = Field(description="Confidence in pattern detection (0-1)")
    problem_alignment: float = Field(description="How well code aligns with problem (0-1)")
    data_structures_used: List[str] = Field(description="Data structures identified in code")
    time_complexity: str = Field(description="Estimated time complexity")
    space_complexity: str = Field(description="Estimated space complexity")
    optimization_techniques: List[str] = Field(description="Optimization techniques used")
    potential_issues: List[str] = Field(description="Potential issues or improvements")
    analysis_quality: str = Field(description="Quality of analysis: high/medium/low")
    execution_steps: Optional[List[ExecutionStepResponse]] = Field(default=None, description="Step-by-step execution trace")
    total_execution_steps: Optional[int] = Field(default=None, description="Total number of execution steps")

class AlgorithmAnalysisErrorResponse(BaseModel):
    error: str = Field(description="Error message")
    reason: str = Field(description="Reason for analysis failure")

class CodeAnalysisResponse(BaseModel):
    status: str = Field(description="Processing status")
    message: str = Field(description="Human-readable status message")
    phases_completed: List[str] = Field(description="Analysis phases completed")

    # Phase 1 Results
    problem_analysis: ProblemAnalysisResponse
    code_metadata: CodeMetadataResponse

    # Phase 2 Results
    algorithm_analysis: Union[AlgorithmAnalysisResponse, AlgorithmAnalysisErrorResponse]

# Debug Response Models
class CodeStructureDebug(BaseModel):
    functions: List[Dict[str, Any]] = Field(description="Function analysis details")
    variables: Dict[str, str] = Field(description="Variable type mappings")
    data_structures: List[str] = Field(description="Data structures found")
    control_flow: List[str] = Field(description="Control flow patterns")
    complexity_indicators: Dict[str, str] = Field(description="Complexity indicators")
    return_pattern: Optional[str] = Field(description="Return statement pattern")

class PatternMatchingDebug(BaseModel):
    primary_pattern: Optional[str] = Field(description="Best matching pattern")
    confidence: float = Field(description="Confidence score")
    all_scores: Dict[str, float] = Field(description="All pattern scores")

class Phase2Debug(BaseModel):
    code_structure: CodeStructureDebug
    pattern_matching: PatternMatchingDebug
    ast_node_count: int = Field(description="Number of AST nodes")

class Phase1Debug(BaseModel):
    validation_errors: List[str] = Field(description="Validation errors found")
    cleaned_code_length: int = Field(description="Length of cleaned code")
    problem_data: Dict[str, Any] = Field(description="Parsed problem data")
    code_metadata: Dict[str, Any] = Field(description="Code metadata")
    ast_available: bool = Field(description="Whether AST parsing succeeded")

class DebugAnalysisResponse(BaseModel):
    debug_info: Dict[str, Any] = Field(description="Detailed debug information")

# Supported Patterns Response
class SupportedPatternsResponse(BaseModel):
    algorithm_patterns: List[str] = Field(description="Supported algorithm patterns")
    problem_types: List[str] = Field(description="Supported problem types")
    phase2_capabilities: List[str] = Field(description="Phase 2 analysis capabilities")

