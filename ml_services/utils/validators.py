# ml_services/utils/validators.py
import ast
import re
from typing import List, Tuple
from models.internal_models import Language

class CodeValidator:
    """Validates code syntax and basic security patterns."""

    def __init__(self):
        # Keep lists small and conservative to avoid false positives
        self.dangerous_imports = {
            'os', 'subprocess', 'sys', 'shutil', 'socket', 'urllib',
            'requests', 'http', 'ftplib', 'smtplib'
        }
        self.dangerous_functions = {
            'eval', 'exec', 'compile', '__import__', 'getattr', 'setattr',
            'delattr', 'globals', 'locals', 'vars'
        }

    def validate_python_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Return (is_valid, errors)."""
        try:
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            return False, [f"Syntax error: {e.msg} at line {e.lineno}"]

    def check_security(self, code: str, language: Language) -> List[str]:
        """Return a list of warnings for potentially risky patterns."""
        if language != Language.PYTHON:
            return []
        warnings: List[str] = []
        warnings.extend(self._check_python_security(code))
        return warnings

    def _check_python_security(self, code: str) -> List[str]:
        warnings: List[str] = []

        # Basic import scan (best-effort, regex-based)
        import_pattern = r'(?:^|\n)\s*(?:import|from)\s+(\w+)'
        for imp in re.findall(import_pattern, code, re.MULTILINE):
            if imp in self.dangerous_imports:
                warnings.append(f"Potentially dangerous import: {imp}")

        # Function call scan
        for func in self.dangerous_functions:
            if re.search(rf'\b{func}\s*\(', code):
                warnings.append(f"Potentially dangerous function: {func}")

        return warnings
