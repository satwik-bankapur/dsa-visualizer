# ml_services/api/analysis_router.py - Enhanced with Phase 2 Integration
import ast

from fastapi import APIRouter, status, HTTPException
from schemas.analysis_schemas import CodeAnalysisRequest, CodeAnalysisResponse
from config.log_config import get_logger
from core.input_processor import InputProcessor
from core.code_analyzer import CodeAnalyzer

logger = get_logger(__name__)
router = APIRouter(prefix="/analysis", tags=["Code Analysis"])

input_processor = InputProcessor()
code_analyzer = CodeAnalyzer()

@router.post("/", response_model=CodeAnalysisResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Enhanced code analysis endpoint with Phase 1 & 2 integration
    """
    logger.info("New code analysis request received")
    try:
        # Phase 1: Input Processing & Validation
        logger.info("Starting Phase 1: Input Processing & Validation")
        processed_data = input_processor.process_input(
            code=request.code_string,
            problem_statement=request.problem_statement,
            language=request.language,
            test_cases=[tc.model_dump() for tc in (request.test_cases or [])]
        )

        if processed_data.validation_errors:
            logger.warning(f"Validation issues: {processed_data.validation_errors}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Validation failed",
                    "issues": processed_data.validation_errors
                }
            )

        # Phase 2: Code Understanding & Pattern Recognition
        logger.info("Starting Phase 2: Code Understanding & Pattern Recognition")
        algorithm_analysis = None
        if processed_data.code_ast:
            algorithm_analysis = code_analyzer.analyze(processed_data)
        else:
            logger.warning("Skipping Phase 2 - No valid AST available")

        # Prepare comprehensive response
        response_data = {
            "status": "processed",
            "message": "Phase 1 & 2 complete. Input validated, parsed, and analyzed.",
            "phases_completed": ["input_processing", "pattern_recognition"],

            # Phase 1 Results
            "problem_analysis": {
                "problem_type": processed_data.problem_data.problem_type.value if processed_data.problem_data.problem_type else None,
                "title": processed_data.problem_data.title,
                "constraints_count": len(processed_data.problem_data.constraints),
                "test_cases_count": len(processed_data.problem_data.test_cases)
            },

            "code_metadata": {
                "detected_language": processed_data.code_metadata.language.value,
                "function_name": processed_data.code_metadata.function_name,
                "parameters": processed_data.code_metadata.parameters,
                "lines_of_code": len(processed_data.cleaned_code.split('\n'))
            },

            # Phase 2 Results
            "algorithm_analysis": None
        }

        if algorithm_analysis:
            response_data["algorithm_analysis"] = {
                "primary_pattern": algorithm_analysis.primary_pattern.value if algorithm_analysis.primary_pattern else None,
                "confidence_score": round(algorithm_analysis.confidence_score, 3),
                "problem_alignment": round(algorithm_analysis.problem_alignment, 3),
                "data_structures_used": [ds.value for ds in algorithm_analysis.data_structures_used],
                "time_complexity": algorithm_analysis.time_complexity,
                "space_complexity": algorithm_analysis.space_complexity,
                "optimization_techniques": algorithm_analysis.optimization_techniques,
                "potential_issues": algorithm_analysis.potential_issues,
                "analysis_quality": "high" if algorithm_analysis.confidence_score > 0.7 else "medium" if algorithm_analysis.confidence_score > 0.4 else "low"
            }
        else:
            response_data["algorithm_analysis"] = {
                "error": "Could not perform algorithm analysis",
                "reason": "Invalid or unparseable code structure"
            }

        logger.info(f"Analysis complete. Pattern: {algorithm_analysis.primary_pattern if algorithm_analysis else 'None'}")
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal error during analysis",
                "phase": "unknown",
                "message": str(e)
            }
        )

@router.get("/patterns", status_code=status.HTTP_200_OK)
async def get_supported_patterns():
    """Get list of supported algorithm patterns"""
    from models.internal_models import AlgorithmPattern, ProblemType

    return {
        "algorithm_patterns": [pattern.value for pattern in AlgorithmPattern],
        "problem_types": [ptype.value for ptype in ProblemType],
        "phase2_capabilities": [
            "AST-based code structure analysis",
            "Algorithm pattern recognition",
            "Problem-code alignment verification",
            "Complexity estimation",
            "Optimization technique identification",
            "Code quality assessment"
        ]
    }

@router.post("/debug", status_code=status.HTTP_200_OK)
async def debug_analysis(request: CodeAnalysisRequest):
    """Debug endpoint with detailed Phase 1 & 2 analysis breakdown"""
    logger.info("Debug analysis request received")

    try:
        # Phase 1 with detailed logging
        processed_data = input_processor.process_input(
            code=request.code_string,
            problem_statement=request.problem_statement,
            language=request.language,
            test_cases=[tc.model_dump() for tc in (request.test_cases or [])]
        )

        # Phase 2 with detailed analysis
        algorithm_analysis = None
        phase2_debug = {}

        if processed_data.code_ast:
            algorithm_analysis = code_analyzer.analyze(processed_data)

            # Additional debug info from the analyzer
            from ml_services.core.code_analyzer import CodeStructure

            # Re-analyze for debug info
            structure = code_analyzer._analyze_code_structure(processed_data.code_ast)
            pattern_results = code_analyzer._match_algorithm_patterns(
                processed_data.code_ast,
                structure,
                processed_data.problem_data
            )

            phase2_debug = {
                "code_structure": {
                    "functions": structure.functions,
                    "variables": structure.variables,
                    "data_structures": [ds.value for ds in structure.data_structures],
                    "control_flow": structure.control_flow,
                    "complexity_indicators": structure.complexity_indicators,
                    "return_pattern": structure.return_pattern
                },
                "pattern_matching": pattern_results,
                "ast_node_count": len(list(ast.walk(processed_data.code_ast)))
            }

        return {
            "debug_info": {
                "phase1": {
                    "validation_errors": processed_data.validation_errors,
                    "cleaned_code_length": len(processed_data.cleaned_code),
                    "problem_data": processed_data.problem_data.model_dump(),
                    "code_metadata": processed_data.code_metadata.model_dump(),
                    "ast_available": processed_data.code_ast is not None
                },
                "phase2": phase2_debug,
                "algorithm_analysis": algorithm_analysis.model_dump() if algorithm_analysis else None
            }
        }

    except Exception as e:
        logger.error(f"Debug analysis failed: {e}", exc_info=True)
        return {
            "error": str(e),
            "debug_info": "Analysis failed during debug"
        }