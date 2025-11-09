# Simple fallback executor when tracing fails
import ast
from typing import Dict, Any, List
from core.execution_tracker import ExecutionStep
from config.log_config import get_logger

logger = get_logger(__name__)

class SimpleExecutor:
    """Simple code executor without tracing - generates basic steps"""
    
    def __init__(self):
        self.safe_builtins = {
            'len': len, 'range': range, 'enumerate': enumerate,
            'max': max, 'min': min, 'sum': sum,
            'int': int, 'float': float, 'str': str, 'bool': bool,
            'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
            'abs': abs, 'round': round, 'sorted': sorted, 'reversed': reversed,
            'zip': zip, 'all': all, 'any': any, 'print': print
        }
    
    def execute_with_tracing(self, code: str, inputs: Dict[str, Any], function_name: str = None) -> List[ExecutionStep]:
        """Execute code and generate basic steps"""
        logger.info("Using simple executor (no tracing)")
        
        try:
            # Parse code to extract basic structure
            parsed = ast.parse(code)
            
            # Execute code safely
            execution_globals = {'__builtins__': self.safe_builtins}
            execution_locals = inputs.copy()
            
            exec(compile(parsed, '<algorithm>', 'exec'), execution_globals, execution_locals)
            
            # Generate basic steps from AST
            steps = self._generate_steps_from_ast(parsed, function_name, inputs)
            
            logger.info(f"Generated {len(steps)} basic steps")
            return steps
            
        except Exception as e:
            logger.error(f"Simple execution failed: {e}")
            return self._generate_fallback_steps(code, function_name, inputs)
    
    def _generate_steps_from_ast(self, parsed: ast.AST, function_name: str, inputs: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate basic steps from AST analysis"""
        steps = []
        step_number = 1
        
        for node in ast.walk(parsed):
            if isinstance(node, ast.FunctionDef):
                if not function_name or node.name == function_name:
                    # Add function entry step
                    steps.append(ExecutionStep(
                        step_number=step_number,
                        line_number=node.lineno,
                        code_line=f"def {node.name}({', '.join(arg.arg for arg in node.args.args)}):",
                        function_name=node.name,
                        event_type='call',
                        variables_before=inputs.copy(),
                        variables_after=inputs.copy(),
                        variable_changes={},
                        explanation="",
                        is_significant=True
                    ))
                    step_number += 1
                    
                    # Add steps for function body
                    for stmt in node.body:
                        if isinstance(stmt, (ast.Assign, ast.AugAssign, ast.If, ast.While, ast.For, ast.Return)):
                            steps.append(ExecutionStep(
                                step_number=step_number,
                                line_number=stmt.lineno,
                                code_line=ast.unparse(stmt) if hasattr(ast, 'unparse') else str(stmt),
                                function_name=node.name,
                                event_type='line',
                                variables_before={},
                                variables_after={},
                                variable_changes={},
                                explanation="",
                                is_significant=True
                            ))
                            step_number += 1
        
        return steps[:20]  # Limit to 20 steps
    
    def _generate_fallback_steps(self, code: str, function_name: str, inputs: Dict[str, Any]) -> List[ExecutionStep]:
        """Generate minimal fallback steps"""
        lines = code.strip().split('\n')
        steps = []
        
        for i, line in enumerate(lines[:10]):  # Limit to 10 lines
            if line.strip() and not line.strip().startswith('#'):
                steps.append(ExecutionStep(
                    step_number=i + 1,
                    line_number=i + 1,
                    code_line=line.strip(),
                    function_name=function_name or 'main',
                    event_type='line',
                    variables_before={},
                    variables_after={},
                    variable_changes={},
                    explanation="",
                    is_significant=True
                ))
        
        return steps