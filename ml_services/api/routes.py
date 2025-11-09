# from fastapi import APIRouter, HTTPException, status
# import logging
# from models.input_models import AnalyzeCodeRequest
# from models.output_models import AnalysisResponse
# from core.pipeline import AnalysisPipeline
#
# logger = logging.getLogger(__name__)
# router = APIRouter()
#
# # Create a single, reusable instance of the pipeline
# pipeline = AnalysisPipeline()
#
# @router.post("/analyze", response_model=AnalysisResponse)
# async def analyze_code(request: AnalyzeCodeRequest) -> AnalysisResponse:
#     """
#     Main endpoint for code analysis that executes the full pipeline.
#     """
#     try:
#         logger.info(f"Received analysis request for language: {request.language.value}")
#
#         # Execute the entire pipeline with a single call
#         analysis_result = pipeline.run(request)
#
#         return analysis_result
#
#     except ValueError as e:
#         logger.error(f"Validation error: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"message": "Invalid input", "errors": str(e)}
#         )
#     except Exception as e:
#         logger.error(f"Internal processing error: {str(e)}", exc_info=True)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={"message": "An internal error occurred during analysis."}
#         )
#
# # Keep your other routes like /health and /supported-patterns as they are.
# # They are well-designed and do not need changes.