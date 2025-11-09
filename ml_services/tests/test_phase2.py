# test_phase2.py - Comprehensive test suite for Phase 2 functionality

import json
import requests

# Test cases for different algorithm patterns
test_cases = {
    "hash_map_two_sum": {
        "code_string": """def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []""",
        "problem_statement": "Two Sum: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. Constraints: linear time complexity required.",
        "expected_pattern": "hash_map"
    },

    "two_pointers_palindrome": {
        "code_string": """def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True""",
        "problem_statement": "Valid Palindrome: Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases. Use two pointers approach.",
        "expected_pattern": "two_pointers"
    },

    "sliding_window_max_subarray": {
        "code_string": """def max_subarray_length(nums, k):
    left = 0
    max_len = 0
    window_sum = 0
    
    for right in range(len(nums)):
        window_sum += nums[right]
        
        while window_sum > k:
            window_sum -= nums[left]
            left += 1
            
        max_len = max(max_len, right - left + 1)
    
    return max_len""",
        "problem_statement": "Maximum Subarray Length: Find the maximum length of a subarray with sum at most k. Use sliding window technique for optimal solution.",
        "expected_pattern": "sliding_window"
    },

    "binary_search": {
        "code_string": """def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1""",
        "problem_statement": "Binary Search: Given a sorted array nums and a target value, return the index if target is found. If not found, return -1. Use binary search for O(log n) complexity.",
        "expected_pattern": "binary_search"
    },

    "dfs_tree_traversal": {
        "code_string": """def dfs_traversal(root):
    if not root:
        return []
    
    result = []
    visited = set()
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        result.append(node.val)
        
        for child in node.children:
            dfs(child)
    
    dfs(root)
    return result""",
        "problem_statement": "Tree Traversal: Perform depth-first traversal of a tree and return all node values. Use recursive DFS approach to visit all nodes.",
        "expected_pattern": "depth_first_search"
    },

    "dynamic_programming_fibonacci": {
        "code_string": """def fibonacci(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]""",
        "problem_statement": "Fibonacci Number: Calculate the nth Fibonacci number. Use dynamic programming to optimize from exponential to linear time complexity.",
        "expected_pattern": "dynamic_programming"
    },

    "greedy_activity_selection": {
        "code_string": """def activity_selection(activities):
    # Sort by end time
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end_time = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end_time:
            selected.append((start, end))
            last_end_time = end
    
    return selected""",
        "problem_statement": "Activity Selection: Given activities with start and end times, select maximum number of non-overlapping activities. Use greedy algorithm for optimal solution.",
        "expected_pattern": "greedy"
    }
}

def test_phase2_analysis(base_url="http://127.0.0.1:8001"):
    """Test Phase 2 analysis with different algorithm patterns"""

    print("🧪 Testing Phase 2: Code Understanding & Pattern Recognition")
    print("=" * 60)

    results = {}

    for test_name, test_data in test_cases.items():
        print(f"\n📝 Testing: {test_name}")
        print(f"Expected Pattern: {test_data['expected_pattern']}")

        # Prepare request
        request_data = {
            "code_string": test_data["code_string"],
            "problem_statement": test_data["problem_statement"],
            "language": "python",
            "test_cases": []
        }

        try:
            # Send request to analysis endpoint
            response = requests.post(
                f"{base_url}/analysis/",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 202:
                result = response.json()
                algorithm_analysis = result.get("algorithm_analysis", {})

                detected_pattern = algorithm_analysis.get("primary_pattern")
                confidence = algorithm_analysis.get("confidence_score", 0)
                alignment = algorithm_analysis.get("problem_alignment", 0)

                # Check if detection was successful
                pattern_match = detected_pattern == test_data["expected_pattern"]

                results[test_name] = {
                    "expected": test_data["expected_pattern"],
                    "detected": detected_pattern,
                    "confidence": confidence,
                    "alignment": alignment,
                    "pattern_match": pattern_match,
                    "status": "success"
                }

                # Print results
                status_icon = "✅" if pattern_match else "❌"
                print(f"  {status_icon} Detected: {detected_pattern} (confidence: {confidence:.3f})")
                print(f"     Alignment: {alignment:.3f}")
                print(f"     Data Structures: {algorithm_analysis.get('data_structures_used', [])}")
                print(f"     Complexity: {algorithm_analysis.get('time_complexity', 'N/A')} time, {algorithm_analysis.get('space_complexity', 'N/A')} space")

            else:
                print(f"  ❌ Request failed: {response.status_code}")
                print(f"     Error: {response.text}")
                results[test_name] = {
                    "status": "failed",
                    "error": response.text
                }

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            results[test_name] = {
                "status": "exception",
                "error": str(e)
            }

    # Summary
    print("\n" + "=" * 60)
    print("📊 PHASE 2 TEST SUMMARY")
    print("=" * 60)

    successful_tests = [r for r in results.values() if r.get("status") == "success"]
    correct_detections = [r for r in successful_tests if r.get("pattern_match")]

    print(f"Total Tests: {len(test_cases)}")
    print(f"Successful Requests: {len(successful_tests)}")
    print(f"Correct Pattern Detections: {len(correct_detections)}")
    print(f"Accuracy: {len(correct_detections)/len(test_cases)*100:.1f}%")

    # Detailed results
    if successful_tests:
        avg_confidence = sum(r.get("confidence", 0) for r in successful_tests) / len(successful_tests)
        avg_alignment = sum(r.get("alignment", 0) for r in successful_tests) / len(successful_tests)
        print(f"Average Confidence: {avg_confidence:.3f}")
        print(f"Average Alignment: {avg_alignment:.3f}")

    return results

def test_debug_endpoint(base_url="http://127.0.0.1:8001"):
    """Test the debug endpoint for detailed analysis"""

    print("\n🔍 Testing Debug Endpoint")
    print("=" * 40)

    # Use the hash map example for debug testing
    test_data = test_cases["hash_map_two_sum"]
    request_data = {
        "code_string": test_data["code_string"],
        "problem_statement": test_data["problem_statement"],
        "language": "python",
        "test_cases": []
    }

    try:
        response = requests.post(
            f"{base_url}/analysis/debug",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            debug_info = response.json()

            print("✅ Debug endpoint successful")
            print(f"Phase 1 Info:")
            phase1 = debug_info.get("debug_info", {}).get("phase1", {})
            print(f"  - AST Available: {phase1.get('ast_available')}")
            print(f"  - Validation Errors: {len(phase1.get('validation_errors', []))}")
            print(f"  - Code Length: {phase1.get('cleaned_code_length')}")

            print(f"Phase 2 Info:")
            phase2 = debug_info.get("debug_info", {}).get("phase2", {})
            if phase2:
                structure = phase2.get("code_structure", {})
                print(f"  - Functions Found: {len(structure.get('functions', []))}")
                print(f"  - Variables: {len(structure.get('variables', {}))}")
                print(f"  - Data Structures: {structure.get('data_structures', [])}")
                print(f"  - Control Flow: {structure.get('control_flow', [])}")
                print(f"  - AST Nodes: {phase2.get('ast_node_count', 0)}")

                patterns = phase2.get("pattern_matching", {})
                print(f"  - Pattern Scores: {patterns.get('all_scores', {})}")

        else:
            print(f"❌ Debug request failed: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"❌ Debug test exception: {e}")

def test_supported_patterns(base_url="http://127.0.0.1:8001"):
    """Test the supported patterns endpoint"""

    print("\n📋 Testing Supported Patterns Endpoint")
    print("=" * 40)

    try:
        response = requests.get(f"{base_url}/analysis/patterns")

        if response.status_code == 200:
            data = response.json()
            print("✅ Supported patterns retrieved successfully")
            print(f"Algorithm Patterns: {data.get('algorithm_patterns', [])}")
            print(f"Problem Types: {data.get('problem_types', [])}")
            print(f"Phase 2 Capabilities:")
            for capability in data.get('phase2_capabilities', []):
                print(f"  - {capability}")
        else:
            print(f"❌ Request failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Exception: {e}")

def run_comprehensive_phase2_test():
    """Run all Phase 2 tests"""

    print("🚀 COMPREHENSIVE PHASE 2 TESTING SUITE")
    print("="*60)

    base_url = "http://127.0.0.1:8001"

    # Test 1: Main analysis endpoint with different patterns
    results = test_phase2_analysis(base_url)

    # Test 2: Debug endpoint
    test_debug_endpoint(base_url)

    # Test 3: Supported patterns endpoint
    test_supported_patterns(base_url)

    print(f"\n🎯 All tests completed!")
    return results

# Additional utility functions for manual testing
def create_test_request(pattern_type="hash_map"):
    """Create a test request for manual testing"""
    if pattern_type in test_cases:
        test_data = test_cases[pattern_type]
        return {
            "code_string": test_data["code_string"],
            "problem_statement": test_data["problem_statement"],
            "language": "python",
            "test_cases": []
        }
    return None

def format_analysis_response(response_json):
    """Format analysis response for better readability"""
    if "algorithm_analysis" in response_json:
        analysis = response_json["algorithm_analysis"]

        print("🔍 ALGORITHM ANALYSIS RESULTS")
        print("-" * 30)
        print(f"Primary Pattern: {analysis.get('primary_pattern', 'None')}")
        print(f"Confidence Score: {analysis.get('confidence_score', 0):.3f}")
        print(f"Problem Alignment: {analysis.get('problem_alignment', 0):.3f}")
        print(f"Data Structures: {', '.join(analysis.get('data_structures_used', []))}")
        print(f"Time Complexity: {analysis.get('time_complexity', 'N/A')}")
        print(f"Space Complexity: {analysis.get('space_complexity', 'N/A')}")
        print(f"Analysis Quality: {analysis.get('analysis_quality', 'N/A')}")

        if analysis.get('optimization_techniques'):
            print(f"Optimizations: {', '.join(analysis['optimization_techniques'])}")

        if analysis.get('potential_issues'):
            print("Potential Issues:")
            for issue in analysis['potential_issues']:
                print(f"  - {issue}")

if __name__ == "__main__":
    # Run the comprehensive test suite
    run_comprehensive_phase2_test()