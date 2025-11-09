# Unified API router that matches frontend expectations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from config.log_config import get_logger
from core.input_processor import InputProcessor
from core.code_analyzer import CodeAnalyzer
from core.execution_simulator import ExecutionSimulator
from models.internal_models import AlgorithmPattern
import ast

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["Unified API"])

# Frontend-compatible request/response models
class AnalyzeRequest(BaseModel):
    code: str
    customArray: Optional[List[int]] = None
    customTarget: Optional[int] = None

class VisualizationStep(BaseModel):
    type: str
    description: str
    array: Optional[List[int]] = None
    target: Optional[int] = None
    left: Optional[int] = None
    right: Optional[int] = None
    mid: Optional[int] = None
    found: Optional[bool] = None
    explanation: str
    data: Optional[Dict[str, Any]] = None

class AnalyzeResponse(BaseModel):
    algorithm: str
    confidence: float
    steps: List[VisualizationStep]
    metadata: Dict[str, Any]

# Pattern name mapping
PATTERN_MAPPING = {
    AlgorithmPattern.HASH_MAP: "Hash Map",
    AlgorithmPattern.TWO_POINTERS: "Two Pointers", 
    AlgorithmPattern.SLIDING_WINDOW: "Sliding Window",
    AlgorithmPattern.BINARY_SEARCH: "Binary Search",
    AlgorithmPattern.DEPTH_FIRST_SEARCH: "Tree Traversal",
    AlgorithmPattern.DYNAMIC_PROGRAMMING: "Dynamic Programming",
    AlgorithmPattern.GREEDY: "Greedy Algorithm"
}

input_processor = InputProcessor()
code_analyzer = CodeAnalyzer()
execution_simulator = ExecutionSimulator()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code_unified(request: AnalyzeRequest):
    """Unified endpoint that matches frontend expectations"""
    logger.info("Unified analysis request received")
    
    try:
        # Phase 1: Process input
        processed_data = input_processor.process_input(
            code=request.code,
            problem_statement="Algorithm analysis request",
            language="python",
            test_cases=[]
        )

        if processed_data.validation_errors:
            raise HTTPException(status_code=400, detail={"errors": processed_data.validation_errors})

        # Phase 2: Analyze algorithm pattern
        algorithm_analysis = code_analyzer.analyze(processed_data)
        
        if not algorithm_analysis:
            raise HTTPException(status_code=400, detail={"error": "Could not analyze algorithm"})

        # Phase 3: Generate execution steps
        execution_results = execution_simulator.simulate_execution(
            processed_data, 
            algorithm_analysis.primary_pattern
        )

        # Transform to frontend format
        algorithm_name = PATTERN_MAPPING.get(algorithm_analysis.primary_pattern, "Unknown Algorithm")
        
        # Convert execution steps to frontend format
        frontend_steps = []
        execution_steps = execution_results.get('execution_steps', [])
        
        for i, step in enumerate(execution_steps):
            viz_step = VisualizationStep(
                type=_get_frontend_step_type(algorithm_analysis.primary_pattern),
                description=f"Step {i+1}: {step.get('explanation', 'Processing...')}",
                explanation=step.get('explanation', ''),
                data=step.get('visualization_data', {})
            )
            
            # Add algorithm-specific data
            if algorithm_analysis.primary_pattern == AlgorithmPattern.BINARY_SEARCH:
                _add_binary_search_data(viz_step, step, request)
            elif algorithm_analysis.primary_pattern == AlgorithmPattern.TWO_POINTERS:
                _add_two_pointers_data(viz_step, step, request)
                
            frontend_steps.append(viz_step)

        # If no steps generated, create basic steps
        if not frontend_steps:
            frontend_steps = _generate_basic_steps(algorithm_analysis.primary_pattern, request)

        response = AnalyzeResponse(
            algorithm=algorithm_name,
            confidence=algorithm_analysis.confidence_score,
            steps=frontend_steps,
            metadata={
                "pattern": algorithm_analysis.primary_pattern.value,
                "time_complexity": algorithm_analysis.time_complexity,
                "space_complexity": algorithm_analysis.space_complexity,
                "total_steps": len(frontend_steps)
            }
        )

        logger.info(f"Analysis complete: {algorithm_name} with {len(frontend_steps)} steps")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": str(e)})

def _get_frontend_step_type(pattern: AlgorithmPattern) -> str:
    """Get frontend step type from algorithm pattern"""
    mapping = {
        AlgorithmPattern.BINARY_SEARCH: "binary_search",
        AlgorithmPattern.TWO_POINTERS: "two_pointers",
        AlgorithmPattern.SLIDING_WINDOW: "sliding_window",
        AlgorithmPattern.HASH_MAP: "hash_map"
    }
    return mapping.get(pattern, "generic")

def _add_binary_search_data(viz_step: VisualizationStep, step: Dict, request: AnalyzeRequest):
    """Add binary search specific data"""
    viz_data = step.get('visualization_data', {})
    pointers = viz_data.get('pointers', {})
    
    viz_step.array = request.customArray or [1, 3, 5, 7, 9, 11]
    viz_step.target = request.customTarget or 7
    viz_step.left = pointers.get('left')
    viz_step.right = pointers.get('right') 
    viz_step.mid = pointers.get('mid')
    viz_step.found = False  # Will be updated based on step analysis

def _add_two_pointers_data(viz_step: VisualizationStep, step: Dict, request: AnalyzeRequest):
    """Add two pointers specific data"""
    viz_data = step.get('visualization_data', {})
    pointers = viz_data.get('pointers', {})
    
    viz_step.array = request.customArray or [1, 2, 3, 4, 5, 6]
    viz_step.target = request.customTarget or 7
    viz_step.left = pointers.get('left')
    viz_step.right = pointers.get('right')

def _generate_basic_steps(pattern: AlgorithmPattern, request: AnalyzeRequest) -> List[VisualizationStep]:
    """Generate basic steps when execution simulation fails"""
    algorithm_name = PATTERN_MAPPING.get(pattern, "Unknown")
    
    if pattern == AlgorithmPattern.BINARY_SEARCH:
        return _generate_binary_search_steps(request.customArray or [1, 3, 5, 7, 9, 11], 
                                           request.customTarget or 7)
    
    # Generic fallback
    return [VisualizationStep(
        type=_get_frontend_step_type(pattern),
        description=f"{algorithm_name} algorithm detected",
        explanation=f"Analyzing {algorithm_name} implementation...",
        data={"array": request.customArray, "target": request.customTarget}
    )]

def _generate_binary_search_steps(array: List[int], target: int) -> List[VisualizationStep]:
    """Generate binary search steps manually"""
    steps = []
    left, right = 0, len(array) - 1
    
    steps.append(VisualizationStep(
        type="binary_search",
        description=f"Starting Binary Search for target {target}",
        array=array,
        target=target,
        left=left,
        right=right,
        mid=None,
        found=False,
        explanation=f"Initialize: left={left}, right={right}"
    ))
    
    step_count = 1
    while left <= right and step_count < 10:
        mid = (left + right) // 2
        
        steps.append(VisualizationStep(
            type="binary_search", 
            description=f"Step {step_count}: Calculate mid = {mid}",
            array=array,
            target=target,
            left=left,
            right=right,
            mid=mid,
            found=False,
            explanation=f"Mid index is {mid}, value is {array[mid]}"
        ))
        
        if array[mid] == target:
            steps.append(VisualizationStep(
                type="binary_search",
                description=f"Found target {target} at index {mid}!",
                array=array,
                target=target,
                left=left,
                right=right,
                mid=mid,
                found=True,
                explanation=f"Success! Target {target} found at index {mid}"
            ))
            break
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        step_count += 1
    
    return steps