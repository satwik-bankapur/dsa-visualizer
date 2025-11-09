from typing import Dict, Any
from models.internal_models import CodeMetadata, Language
import ast
import re

class ProblemParser:
    def parse(self, problem_statement: str) -> Dict[str, Any]:
        # Minimal but structured parsing
        text = problem_statement.strip()
        title = self._extract_title(text)
        constraints_text = self._extract_constraints_section(text)
        return {
            "text": text,
            "title": title,
            "constraints_text": constraints_text,
            "hints": [],
            "difficulty": None,
            "examples": []
        }

    def _extract_title(self, text: str) -> str:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if not lines:
            return "Unknown Problem"
        first = lines[0]  # pick first line
        if len(first) < 100 and not first.endswith("."):
            return first
        return (first.split(".")[0] if "." in first else first).strip()


    def _extract_constraints_section(self, text: str) -> str:
        m = re.search(r'Constraints?:?\s*(.*?)(?:\n\s*\n|\Z)', text, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else ""

class CodeParser:
    def extract_metadata(self, code: str, language: Language) -> CodeMetadata:
        if language == Language.PYTHON:
            try:
                tree = ast.parse(code)
                func = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)), None)
                if func:
                    params = [a.arg for a in func.args.args]
                    return CodeMetadata(language=language, function_name=func.name, parameters=params)
            except SyntaxError:
                pass
        # Fallback
        return CodeMetadata(language=language, function_name=None, parameters=[])
