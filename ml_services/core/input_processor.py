# core/input_processor.py
import re
import ast
from typing import List, Dict, Any, Optional
from models.internal_models import (
    ProcessedInput, ProblemData, CodeMetadata, TestCase,
    Constraint, Language, ProblemType
)
from utils.parsers import ProblemParser, CodeParser
from utils.validators import CodeValidator

class InputProcessor:
    """Phase 1: Input Processing & Validation"""

    def __init__(self):
        self.problem_parser = ProblemParser()
        self.code_parser = CodeParser()
        self.code_validator = CodeValidator()
        self.supported_languages = [lang.value for lang in Language]

    def process_input(
            self,
            code: str,
            problem_statement: str,
            language: Language,
            test_cases: List[Dict[str, Any]] = None
    ) -> ProcessedInput:

        validation_errors: List[str] = []

        # input reception
        validation_errors.extend(self._validate_input_reception(code, problem_statement, language))

        # sanitize + security + syntax
        cleaned_code = self._sanitize_code(code)

        security_warnings = self.code_validator.check_security(cleaned_code, language)
        if security_warnings:
            validation_errors.extend(security_warnings)

        is_valid_syntax, syntax_errors = self.code_validator.validate_python_syntax(cleaned_code)
        if not is_valid_syntax:
            validation_errors.extend(syntax_errors)

        # Build AST (best-effort)
        code_ast = None
        try:
            code_ast = ast.parse(cleaned_code)
        except SyntaxError:
            pass

        #  problem parsing and assembly
        parsed_problem = self.problem_parser.parse(problem_statement)
        problem_data = self._analyze_problem_statement(parsed_problem, test_cases)

        # Code metadata
        code_metadata = self.code_parser.extract_metadata(cleaned_code, language)

        # Select test case
        selected_test_case = self._select_test_case(problem_data.test_cases)

        return ProcessedInput(
            original_code=code,
            cleaned_code=cleaned_code,
            problem_data=problem_data,
            code_metadata=code_metadata,
            selected_test_case=selected_test_case,
            validation_errors=validation_errors,
            code_ast=code_ast
        )

    # ml_services/core/input_processor.py - Enhanced fix

    def _validate_input_reception(self, code: str, problem_statement: str, language) -> List[str]:
        """Validate basic input reception with proper language handling"""
        validation_errors = []

        # Handle both string and enum input for language
        if hasattr(language, 'value'):
            # It's an enum object
            language_str = language.value
        else:
            # It's already a string
            language_str = str(language).lower()

        # Now validate the language string
        if language_str not in self.supported_languages:
            validation_errors.append(
                f"Unsupported language: {language_str}. "
                f"Supported: {', '.join(self.supported_languages)}"
            )

        # Validate other inputs
        if not code or not code.strip():
            validation_errors.append("Code cannot be empty")

        if not problem_statement or not problem_statement.strip():
            validation_errors.append("Problem statement cannot be empty")

        return validation_errors


    def _sanitize_code(self, code: str) -> str:
        return code.strip()

    def _analyze_problem_statement(self, parsed_problem: Dict[str, Any], test_cases_input: List[Dict[str, Any]] = None) -> ProblemData:
        constraints = self._extract_constraints(parsed_problem.get('constraints_text', ''))
        test_cases: List[TestCase] = []
        if test_cases_input:
            test_cases = [TestCase(**tc) for tc in test_cases_input]

        problem_type = self._classify_problem_type(parsed_problem.get('text', ''))
        return ProblemData(
            title=parsed_problem.get('title', 'Unknown Problem'),
            description=parsed_problem.get('text', ''),
            constraints=constraints,
            test_cases=test_cases,
            problem_type=problem_type
        )

    def _extract_constraints(self, problem_text: str) -> List[Constraint]:
        constraints: List[Constraint] = []
        for pat in [r'O\(([^)]+)\)', r'linear time', r'constant time']:
            for m in re.finditer(pat, problem_text, re.IGNORECASE):
                constraints.append(Constraint(
                    type='time_complexity',
                    value=m.group(1) if m.groups() else m.group(0)
                ))
        return constraints

    def _classify_problem_type(self, problem_text: str) -> Optional[ProblemType]:
        text_lower = problem_text.lower()
        mapping = {
            ProblemType.ARRAY: ['array', 'list'],
            ProblemType.STRING: ['string', 'character'],
            ProblemType.TREE: ['tree', 'binary tree', 'node'],
            ProblemType.GRAPH: ['graph', 'vertex', 'edge', 'path'],
        }
        for ptype, kws in mapping.items():
            if any(k in text_lower for k in kws):
                return ptype
        return None

    def _select_test_case(self, test_cases: List[TestCase]) -> Optional[TestCase]:
        return test_cases[0] if test_cases else None
