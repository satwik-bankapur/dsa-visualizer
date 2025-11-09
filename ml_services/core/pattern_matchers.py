# ml_services/core/pattern_matchers.py - Additional Pattern Recognition Methods

import ast
from typing import Dict, List, Any, Optional, Set
from models.internal_models import AlgorithmPattern, DataStructureType
from config.log_config import get_logger

logger = get_logger(__name__)


class PatternMatchers:
    """Collection of specialized pattern matching methods for different algorithms."""

    def __init__(self):
        self.matchers = {
            AlgorithmPattern.HASH_MAP: self._match_hash_map_pattern,
            AlgorithmPattern.TWO_POINTERS: self._match_two_pointers_pattern,
            AlgorithmPattern.SLIDING_WINDOW: self._match_sliding_window_pattern,
            AlgorithmPattern.BINARY_SEARCH: self._match_binary_search_pattern,
            AlgorithmPattern.DEPTH_FIRST_SEARCH: self._match_dfs_pattern,
            AlgorithmPattern.DYNAMIC_PROGRAMMING: self._match_dp_pattern,
            AlgorithmPattern.GREEDY: self._match_greedy_pattern,
        }

    # ---------------------------
    # Hash Map (dict) detection
    # ---------------------------
    def _match_hash_map_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Stricter hash map matching: only count dict operations on known dict bases."""
        score = 0.0

        # 1) Collect names that are dict-like
        dict_names: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Explicit dict literal: {...}
                if isinstance(node.value, ast.Dict):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            dict_names.add(t.id)
                # dict() constructor
                elif (
                        isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == "dict"
                ):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            dict_names.add(t.id)
                else:
                    # Heuristic by variable name
                    for t in node.targets:
                        if isinstance(t, ast.Name) and any(
                                k in t.id.lower()
                                for k in ("map", "memo", "seen", "cache", "lookup")
                        ):
                            dict_names.add(t.id)

        dict_ops = {"creation": False, "insertion": False, "lookup": False, "in_loop": False}

        # 2) Walk to find dict operations (restricted to known dict names)
        for node in ast.walk(tree):
            # Dict literal creation gives a small boost
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                dict_ops["creation"] = True
                score += 0.2

            # Lookups and updates inside loops
            elif isinstance(node, (ast.For, ast.While)):
                for sub in ast.walk(node):
                    # Lookup: d[key]
                    if isinstance(sub, ast.Subscript):
                        base = getattr(sub.value, "id", None)
                        if base in dict_names:
                            dict_ops["lookup"] = True
                            dict_ops["in_loop"] = True
                            score += 0.25
                    # Insertion/update: d[key] = ...
                    elif isinstance(sub, ast.Assign):
                        for tgt in sub.targets:
                            if isinstance(tgt, ast.Subscript):
                                base = getattr(tgt.value, "id", None)
                                if base in dict_names:
                                    dict_ops["insertion"] = True
                                    score += 0.2

            # Membership: if key in d:
            elif isinstance(node, ast.Compare) and any(isinstance(op, ast.In) for op in node.ops):
                # Count only if the RHS has a dict-like name (best-effort check over names)
                names = [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]
                if any(n in dict_names for n in names):
                    score += 0.15

        # 3) Bonus for a complete dict-in-loop lookup pattern
        if dict_ops["creation"] and dict_ops["lookup"] and dict_ops["in_loop"]:
            score += 0.2

        # 4) Problem context hint
        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("two sum", "lookup", "complement", "pair", "indices")):
            score += 0.1

        return min(score, 1.0)

    # ---------------------------
    # Two Pointers
    # ---------------------------
    def _match_two_pointers_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Two pointers: increment/decrement without mid logic; avoid hijacking binary search."""
        score = 0.0
        pointer_names = {"left", "right", "start", "end", "low", "high", "i", "j"}
        found = set()
        moved = False
        convergence = False
        mid_present = False

        for node in ast.walk(tree):
            # Pointer presence
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id.lower() in pointer_names:
                        found.add(t.id.lower())
            # Pointer movement
            if isinstance(node, ast.AugAssign):
                if isinstance(node.target, ast.Name) and node.target.id.lower() in pointer_names:
                    moved = True
                    score += 0.2
            # Convergence while-condition
            if isinstance(node, ast.While) and isinstance(node.test, ast.Compare):
                names = [n.id.lower() for n in ast.walk(node.test) if isinstance(n, ast.Name)]
                if any(n in pointer_names for n in names):
                    convergence = True
                    score += 0.2
            # mid presence indicates binary search
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and "mid" in t.id.lower():
                        mid_present = True

        if len(found) >= 2:
            score += 0.3
        if moved and convergence:
            score += 0.2

        # Suppress if mid detected (to avoid mislabeling binary search)
        if mid_present:
            score = min(score, 0.2)

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(keyword in desc for keyword in ("sorted", "palindrome", "two sum", "container")):
            score += 0.1

        return min(score, 1.0)

    # ---------------------------
    # Sliding Window
    # ---------------------------
    def _match_sliding_window_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Detect sliding window: expand with right, shrink with left, track best length/score."""
        score = 0.0
        has_left_init_zero = False
        has_for_right_range = False
        has_shrink_while = False
        left_inc_in_while = False
        tracks_best_len = False

        for node in ast.walk(tree):
            # left = 0
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id.lower() == "left":
                        if isinstance(node.value, ast.Constant) and node.value.value == 0:
                            has_left_init_zero = True
                            score += 0.1

            # for right in range(len(...))
            if isinstance(node, ast.For):
                if isinstance(node.target, ast.Name) and node.target.id.lower() == "right":
                    if (
                            isinstance(node.iter, ast.Call)
                            and isinstance(node.iter.func, ast.Name)
                            and node.iter.func.id == "range"
                    ):
                        has_for_right_range = True
                        score += 0.2

            # while condition that shrinks from left
            if isinstance(node, ast.While):
                has_shrink_while = True
                for sub in ast.walk(node):
                    if (
                            isinstance(sub, ast.AugAssign)
                            and isinstance(sub.target, ast.Name)
                            and sub.target.id.lower() == "left"
                            and isinstance(sub.op, ast.Add)
                    ):
                        left_inc_in_while = True
                        score += 0.2

            # best length tracking: max_len = max(max_len, right - left + 1)
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    if node.value.func.id in ("max", "min"):
                        tracks_best_len = True
                        score += 0.2

        # Full pattern
        if has_left_init_zero and has_for_right_range and has_shrink_while and left_inc_in_while and tracks_best_len:
            score += 0.3

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("substring", "subarray", "window", "longest", "maximum", "sliding window")):
            score += 0.1

        return min(score, 1.0)

    # ---------------------------
    # Binary Search
    # ---------------------------
    def _match_binary_search_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Detect binary search with strong signals."""
        score = 0.0
        has_mid = False
        while_with_bounds = False
        updates_lr = False

        for node in ast.walk(tree):
            # mid = (left + right) // 2
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and "mid" in t.id.lower():
                        if isinstance(node.value, ast.BinOp):
                            has_mid = True
                            score += 0.4
            # while left <= right
            if isinstance(node, ast.While):
                if isinstance(node.test, ast.Compare):
                    names = [n.id.lower() for n in ast.walk(node.test) if isinstance(n, ast.Name)]
                    if any(n in ("left", "low") for n in names) and any(n in ("right", "high") for n in names):
                        while_with_bounds = True
                        score += 0.2
            # updates to left/right based on comparisons
            if isinstance(node, ast.If):
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Assign):
                        for tt in sub.targets:
                            if isinstance(tt, ast.Name) and tt.id.lower() in ("left", "right", "low", "high"):
                                updates_lr = True
                                score += 0.2

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("sorted", "search", "binary search", "log")):
            score += 0.1

        # Strong completion bonus
        if has_mid and while_with_bounds and updates_lr:
            score += 0.2

        return min(score, 1.0)

    # ---------------------------
    # Depth-First Search (DFS)
    # ---------------------------
    def _match_dfs_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Detect depth-first search pattern."""
        score = 0.0
        has_recursion = False
        has_visited_tracking = False
        has_stack_usage = False
        has_graph_traversal = False

        for node in ast.walk(tree):
            # Recursion: function calling itself
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        if child.func.id == node.name:
                            has_recursion = True
                            score += 0.4

            # visited set/array
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and "visit" in t.id.lower():
                        has_visited_tracking = True
                        score += 0.2

            # stack usage (.append/.pop)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ("append", "pop"):
                    has_stack_usage = True
                    score += 0.1

            # iterate neighbors/children
            if isinstance(node, ast.For) and isinstance(node.iter, ast.Attribute):
                attr_name = node.iter.attr.lower()
                if any(k in attr_name for k in ("children", "neighbors", "adjacent")):
                    has_graph_traversal = True
                    score += 0.2

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("tree", "graph", "path", "traverse", "connected")):
            score += 0.1

        return min(score, 1.0)

    # ---------------------------
    # Dynamic Programming (DP)
    # ---------------------------
    def _match_dp_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Detect DP via dp array/table + recurrence over prior dp entries (1D or 2D)."""
        score = 0.0
        dp_names: Set[str] = set()
        dp_fill = False
        recurrence = False

        for node in ast.walk(tree):
            # dp = [0] * (n+1) OR explicit list/dict
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and "dp" in t.id.lower():
                        # list or dict
                        if isinstance(node.value, (ast.List, ast.Dict)):
                            dp_names.add(t.id)
                            score += 0.3
                        # list repetition, e.g., [0] * (n+1)
                        elif isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Mult) and isinstance(node.value.left, ast.List):
                            dp_names.add(t.id)
                            score += 0.3

            # dp[i] = dp[i-1] + dp[i-2]
            if isinstance(node, ast.Assign):
                if any(
                        isinstance(t, ast.Subscript)
                        and isinstance(getattr(t.value, "id", None), str)
                        and t.value.id in dp_names
                        for t in node.targets
                ):
                    dp_fill = True
                    # RHS uses dp[...] with +/- on indices
                    rhs_has_dp = any(
                        isinstance(n, ast.Name) and n.id in dp_names
                        for n in ast.walk(node.value)
                    )
                    rhs_has_index_math = any(
                        isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Sub, ast.Add))
                        for n in ast.walk(node.value)
                    )
                    if rhs_has_dp and rhs_has_index_math:
                        recurrence = True
                        score += 0.3

        if dp_fill and recurrence:
            score += 0.3

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("optimal", "maximum", "minimum", "count ways", "fibonacci", "dynamic programming", "dp")):
            score += 0.1

        return min(score, 1.0)

    # ---------------------------
    # Greedy
    # ---------------------------
    def _match_greedy_pattern(self, tree: ast.AST, structure, problem_data) -> float:
        """Detect greedy algorithm pattern: sort + local optimum + single pass."""
        score = 0.0
        has_sorting = False
        has_local_optimal = False
        has_single_pass = False

        for node in ast.walk(tree):
            # sorting
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                    has_sorting = True
                    score += 0.3
                elif isinstance(node.func, ast.Name) and node.func.id == "sorted":
                    has_sorting = True
                    score += 0.3

            # local optimal checks via max/min usage
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("max", "min"):
                    has_local_optimal = True
                    score += 0.2

            # single pass (for without nested for)
            if isinstance(node, ast.For):
                nested_for = any(isinstance(n, ast.For) and n is not node for n in ast.walk(node))
                if not nested_for:
                    has_single_pass = True
                    score += 0.1

        desc = (getattr(problem_data, "description", "") or "").lower()
        if any(k in desc for k in ("greedy", "interval", "schedule", "minimum", "maximum")):
            score += 0.2

        return min(score, 1.0)
