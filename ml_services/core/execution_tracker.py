# ml_services/core/execution_tracker.py
import sys
import ast
import copy
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from config.log_config import get_logger

logger = get_logger(__name__)

@dataclass
class ExecutionStep:
    """Represents one step in algorithm execution"""
    step_number: int
    line_number: int
    code_line: str
    function_name: str
    event_type: str  # 'line', 'call', 'return'
    variables_before: Dict[str, Any] = field(default_factory=dict)
    variables_after: Dict[str, Any] = field(default_factory=dict)
    variable_changes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    explanation: str = ""
    visualization_data: Dict[str, Any] = field(default_factory=dict)
    is_significant: bool = True

class ExecutionTracker:
    """Tracks code execution line-by-line with variable state capture"""

    def __init__(self, target_function_name: str = None):
        self.steps: List[ExecutionStep] = []
        self.step_counter = 0
        self.function_locals_history: Dict[str, Dict[str, Any]] = {}
        self.target_function = target_function_name

    def trace_execution(self, frame, event: str, arg):
        """Main trace function called by sys.settrace()"""
        try:
            code = frame.f_code
            func_name = code.co_name
            line_no = frame.f_lineno

            # Skip if not our target function
            if self.target_function and func_name != self.target_function:
                return self.trace_execution

            # Skip built-in functions
            if func_name.startswith('<') or 'importlib' in str(code.co_filename):
                return self.trace_execution

            # Get current line of code
            code_line = f"<line {line_no}>"

            if event == 'line':
                self._handle_line_event(frame, code_line, func_name, line_no)
            elif event == 'call':
                self._handle_call_event(frame, func_name, line_no)
            elif event == 'return':
                self._handle_return_event(frame, func_name, arg)

        except Exception as e:
            logger.error(f"Error in trace_execution: {e}")

        return self.trace_execution

    def _handle_line_event(self, frame, code_line: str, func_name: str, line_no: int):
        """Handle line execution events"""
        current_locals = self._safe_copy_locals(frame.f_locals)
        prev_locals = self.function_locals_history.get(func_name, {})
        changes = self._detect_variable_changes(prev_locals, current_locals)

        if changes or self.step_counter < 10:  # Always include first 10 steps
            step = ExecutionStep(
                step_number=self.step_counter,
                line_number=line_no,
                code_line=code_line.strip(),
                function_name=func_name,
                event_type='line',
                variables_before=copy.deepcopy(prev_locals),
                variables_after=copy.deepcopy(current_locals),
                variable_changes=changes,
                is_significant=True
            )

            self.steps.append(step)
            self.step_counter += 1

        self.function_locals_history[func_name] = current_locals

    def _handle_call_event(self, frame, func_name: str, line_no: int):
        """Handle function call events"""
        if func_name != '<module>':
            current_locals = self._safe_copy_locals(frame.f_locals)

            step = ExecutionStep(
                step_number=self.step_counter,
                line_number=line_no,
                code_line=f"def {func_name}(...)",
                function_name=func_name,
                event_type='call',
                variables_after=copy.deepcopy(current_locals),
                is_significant=True
            )

            self.steps.append(step)
            self.step_counter += 1
            self.function_locals_history[func_name] = current_locals

    def _handle_return_event(self, frame, func_name: str, return_value):
        """Handle function return events"""
        step = ExecutionStep(
            step_number=self.step_counter,
            line_number=frame.f_lineno,
            code_line=f"return {return_value}",
            function_name=func_name,
            event_type='return',
            variable_changes={'return_value': {'new': return_value}},
            is_significant=True
        )

        self.steps.append(step)
        self.step_counter += 1

    def _detect_variable_changes(self, old_vars: Dict, new_vars: Dict) -> Dict[str, Dict[str, Any]]:
        """Detect and categorize variable changes"""
        changes = {}

        # New variables
        for var, value in new_vars.items():
            if var not in old_vars:
                changes[var] = {'type': 'new', 'new': value}

        # Modified variables
        for var, new_value in new_vars.items():
            if var in old_vars and old_vars[var] != new_value:
                changes[var] = {'type': 'modified', 'old': old_vars[var], 'new': new_value}

        return changes

    def _safe_copy_locals(self, locals_dict: Dict) -> Dict[str, Any]:
        """Safely copy locals, handling unpicklable objects"""
        safe_locals = {}

        for key, value in locals_dict.items():
            try:
                if key.startswith('_'):
                    continue
                safe_locals[key] = copy.deepcopy(value)
            except:
                try:
                    safe_locals[key] = str(value)
                except:
                    safe_locals[key] = f"<{type(value).__name__}>"

        return safe_locals