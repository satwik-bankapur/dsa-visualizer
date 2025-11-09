# from models.input_models import AnalyzeCodeRequest
# from models.output_models import AnalysisResponse
# from .input_processor import InputProcessor
# from .code_analyzer import CodeAnalyzer
#
# class AnalysisPipeline:
#     """Orchestrates the entire code analysis pipeline."""
#     def __init__(self):
#         self.input_processor = InputProcessor()
#         self.code_analyzer = CodeAnalyzer()
#
#     def run(self, request: AnalyzeCodeRequest) -> AnalysisResponse:
#         # Phase 1
#         processed_input = self.input_processor.process_input(
#             code=request.code,
#             problem_statement=request.problem_statement,
#             language=request.language,
#             test_cases=[tc.dict() for tc in request.test_cases] if request.test_cases else None
#         )
#
#         if processed_input.validation_errors:
#             raise ValueError(", ".join(processed_input.validation_errors))
#
#         # Phase 2
#         algorithm_pattern = self.code_analyzer.analyze(processed_input)
#
#         # Build and return the final response
#         return AnalysisResponse(
#             success=True,
#             problem_type=processed_input.problem_data.problem_type,
#             algorithm_pattern=algorithm_pattern,
#             total_steps=0,
#             steps=[],
#             metadata={"detected_pattern": algorithm_pattern.value if algorithm_pattern else "None"}
#         )