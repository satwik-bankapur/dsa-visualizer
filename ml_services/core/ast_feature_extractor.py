import ast
from typing import Dict, List, Any
from collections import Counter, defaultdict

class ASTFeatureExtractor:
    """Extract numerical features from Python AST for ML training"""

    def __init__(self):
        self.feature_names_ = []

    def extract_features(self, code_ast: ast.AST, code_text: str = "") -> Dict[str, float]:
        """Extract comprehensive features from AST"""
        features = {}

        # 1. Node type counts
        node_counts = self._count_node_types(code_ast)
        features.update(node_counts)

        # 2. Structural features
        structural = self._extract_structural_features(code_ast)
        features.update(structural)

        # 3. Control flow features
        control_flow = self._extract_control_flow_features(code_ast)
        features.update(control_flow)

        # 4. Variable and function features
        var_func = self._extract_variable_function_features(code_ast)
        features.update(var_func)

        # 5. Code text features (basic)
        text_features = self._extract_text_features(code_text)
        features.update(text_features)

        return features

    def _count_node_types(self, tree: ast.AST) -> Dict[str, int]:
        """Count different AST node types"""
        counts = Counter()
        for node in ast.walk(tree):
            counts[type(node).__name__] += 1

        # Convert to standardized feature dict
        node_features = {}
        important_nodes = [
            'FunctionDef', 'For', 'While', 'If', 'Assign', 'AugAssign',
            'Call', 'Subscript', 'Dict', 'List', 'Set', 'Compare',
            'BinOp', 'BoolOp', 'Return', 'Break', 'Continue'
        ]

        for node_type in important_nodes:
            node_features[f'count_{node_type.lower()}'] = counts.get(node_type, 0)

        return node_features

    def _extract_structural_features(self, tree: ast.AST) -> Dict[str, float]:
        """Extract structural complexity features"""
        features = {}

        # Tree depth
        features['tree_depth'] = self._calculate_tree_depth(tree)

        # Nested loop depth
        features['max_nested_loops'] = self._max_nested_loops(tree)

        # Function count and average complexity
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        features['function_count'] = len(functions)

        if functions:
            avg_func_complexity = sum(len([n for n in ast.walk(f)]) for f in functions) / len(functions)
            features['avg_function_complexity'] = avg_func_complexity
        else:
            features['avg_function_complexity'] = 0

        return features

    def _extract_control_flow_features(self, tree: ast.AST) -> Dict[str, float]:
        """Extract control flow pattern features"""
        features = {}

        # Loop patterns
        for_loops = [n for n in ast.walk(tree) if isinstance(n, ast.For)]
        while_loops = [n for n in ast.walk(tree) if isinstance(n, ast.While)]

        features['for_loop_count'] = len(for_loops)
        features['while_loop_count'] = len(while_loops)

        # Conditional patterns
        if_statements = [n for n in ast.walk(tree) if isinstance(n, ast.If)]
        features['if_count'] = len(if_statements)

        # Binary operations (indicators of calculations)
        bin_ops = [n for n in ast.walk(tree) if isinstance(n, ast.BinOp)]
        features['binary_op_count'] = len(bin_ops)

        # Comparison operations (indicators of conditions)
        comparisons = [n for n in ast.walk(tree) if isinstance(n, ast.Compare)]
        features['comparison_count'] = len(comparisons)

        return features

    def _extract_variable_function_features(self, tree: ast.AST) -> Dict[str, float]:
        """Extract variable and function usage patterns"""
        features = {}

        # Variable assignments
        assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
        features['assignment_count'] = len(assignments)

        # Function calls
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        features['function_call_count'] = len(calls)

        # Subscript operations (array/dict access)
        subscripts = [n for n in ast.walk(tree) if isinstance(n, ast.Subscript)]
        features['subscript_count'] = len(subscripts)

        # Return statements
        returns = [n for n in ast.walk(tree) if isinstance(n, ast.Return)]
        features['return_count'] = len(returns)

        return features

    def _extract_text_features(self, code_text: str) -> Dict[str, float]:
        """Extract basic text-based features"""
        features = {}

        lines = code_text.split('\n')
        features['line_count'] = len(lines)
        features['char_count'] = len(code_text)
        features['avg_line_length'] = sum(len(line) for line in lines) / max(len(lines), 1)

        # Keyword presence (pattern indicators)
        keywords = {
            'has_range': 'range(' in code_text,
            'has_enumerate': 'enumerate(' in code_text,
            'has_len': 'len(' in code_text,
            'has_max': 'max(' in code_text,
            'has_min': 'min(' in code_text,
            'has_sort': '.sort(' in code_text or 'sorted(' in code_text,
            'has_append': '.append(' in code_text,
            'has_pop': '.pop(' in code_text,
        }

        for key, value in keywords.items():
            features[key] = float(value)

        return features

    def _calculate_tree_depth(self, tree: ast.AST, depth: int = 0) -> int:
        """Calculate maximum depth of AST"""
        if not hasattr(tree, '_fields'):
            return depth

        max_child_depth = depth
        for field_name, field_value in ast.iter_fields(tree):
            if isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, ast.AST):
                        child_depth = self._calculate_tree_depth(item, depth + 1)
                        max_child_depth = max(max_child_depth, child_depth)
            elif isinstance(field_value, ast.AST):
                child_depth = self._calculate_tree_depth(field_value, depth + 1)
                max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def _max_nested_loops(self, tree: ast.AST) -> int:
        """Calculate maximum nested loop depth"""
        max_depth = 0

        def count_nested_depth(node, current_depth=0):
            nonlocal max_depth

            if isinstance(node, (ast.For, ast.While)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)

            for child in ast.iter_child_nodes(node):
                count_nested_depth(child, current_depth)

        count_nested_depth(tree)
        return max_depth
