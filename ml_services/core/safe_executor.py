import sys
import signal
import ast
import types
import threading
import time
import platform
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
from core.execution_tracker import ExecutionTracker, ExecutionStep
from config.log_config import get_logger

logger = get_logger(__name__)

class TimeoutException(Exception):
    """Raised when code execution exceeds time limit"""
    pass

class SafeExecutor:
    """Executes code safely with resource limits and sandboxing"""

    def __init__(self,
                 timeout_seconds: int = 10,
                 memory_limit_mb: int = 100):
        self.timeout_seconds = timeout_seconds
        self.memory_limit_mb = memory_limit_mb
        self.restricted_globals = self._create_restricted_globals()

    def execute_with_tracing(self,
                             code: str,
                             inputs: Dict[str, Any],
                             function_name: str = None) -> List[ExecutionStep]:
        """Execute code with full execution tracing"""

        # CHECK: Threading compatibility first
        if threading.active_count() > 1:
            raise ValueError("Code tracing not supported in multi-threaded environment")

        # Parse and validate the code
        try:
            parsed = ast.parse(code)
            self._validate_ast(parsed)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in code: {e}")
        except Exception as e:
            raise ValueError(f"Invalid code: {e}")

        # Set up execution tracker
        tracker = ExecutionTracker(target_function_name=function_name)

        # Store original trace function to restore later
        original_trace = sys.gettrace()

        # Execute with timeout and tracing
        try:
            with self._timeout_context():
                # Set up execution environment
                execution_globals = self.restricted_globals.copy()
                execution_locals = inputs.copy()

                # Install tracer
                sys.settrace(tracker.trace_execution)

                # Execute the code
                exec(compile(parsed, '<algorithm>', 'exec'), execution_globals, execution_locals)

                return tracker.steps

        except TimeoutException:
            raise ValueError(f"Code execution timed out after {self.timeout_seconds} seconds")
        except RecursionError:
            raise ValueError("Code execution caused infinite recursion")
        except Exception as e:
            logger.error(f"Error during code execution: {e}")
            raise ValueError(f"Execution error: {e}")
        finally:
            # CRITICAL: Always restore original trace function
            sys.settrace(original_trace)

    def _create_restricted_globals(self) -> Dict[str, Any]:
        """Create a restricted global environment for code execution"""

    # ONLY allow these safe functions
        safe_builtins = {
            'len': len, 'range': range, 'enumerate': enumerate,
            'max': max, 'min': min, 'sum': sum,
            'int': int, 'float': float, 'str': str, 'bool': bool,
            'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
            # Safe operations
            'abs': abs, 'round': round, 'sorted': sorted, 'reversed': reversed,
            'zip': zip, 'all': all, 'any': any,
            # ADD THIS: Allow print for debugging/output
            'print': print,  # ← ADD THIS LINE
        }
        return {'__builtins__': safe_builtins}


    def _validate_ast(self, node: ast.AST):
        """Validate AST to ensure only safe operations are used"""

        # Forbidden node types
        forbidden_nodes = {
            ast.Import,      # No imports
            ast.ImportFrom,  # No imports
            # Note: ast.Exec and ast.Eval don't exist in Python 3
        }

        # Forbidden function calls
        forbidden_calls = {
            'exec', 'eval', 'compile', '__import__', 'open',
            'input', 'raw_input', 'file', 'execfile',
            'reload', 'vars', 'locals', 'globals', 'dir',
            'getattr', 'setattr', 'delattr', 'hasattr'
        }

        for node in ast.walk(node):
            # Check forbidden node types
            if type(node) in forbidden_nodes:
                raise ValueError(f"Forbidden operation: {type(node).__name__}")

            # Check forbidden function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                    raise ValueError(f"Forbidden function call: {node.func.id}")

                # Check attribute calls that might be dangerous
                if isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    if attr_name in ['__import__', '__getattribute__', '__setattr__']:
                        raise ValueError(f"Forbidden method call: {attr_name}")

    @contextmanager
    def _timeout_context(self):
        """Context manager for execution timeout - handles both Windows and Unix"""

        timeout_occurred = False

        if platform.system() == 'Windows':
            # Windows: Use threading.Timer
            def timeout_handler():
                nonlocal timeout_occurred
                timeout_occurred = True

            timer = threading.Timer(self.timeout_seconds, timeout_handler)
            timer.start()

            try:
                yield
                if timeout_occurred:
                    raise TimeoutException("Code execution timed out")
            finally:
                timer.cancel()

        else:
            # Unix/Linux: Use signal.SIGALRM
            def timeout_handler(signum, frame):
                raise TimeoutException("Code execution timed out")

            # Set up signal handler for timeout
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.timeout_seconds)

            try:
                yield
            finally:
                # Clean up
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
