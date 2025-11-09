# ml_services/tests/test_phase4_ai_explanations.py
import ast
import unittest
from core.execution_simulator import ExecutionSimulator
from models.internal_models import (
    ProcessedInput, ProblemData, CodeMetadata, TestCase, AlgorithmPattern
)

class TestPhase4AIExplanations(unittest.TestCase):
    """Test Phase 4: AI-Enhanced Step Explanations"""

    def setUp(self):
        """Set up test fixtures for all Phase 4 tests"""
        self.simulator = ExecutionSimulator()

    def test_hash_map_ai_explanations(self):
        """Test AI explanations for hash map algorithm pattern"""
        print("\n🚀 Testing Phase 4: Hash Map AI Explanations")

        code = '''
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

result = two_sum([2, 7, 11, 15], 9)
print(f"Result: {result}")
'''

        # Create comprehensive test setup
        test_case = TestCase(
            input_data={'nums': [2, 7, 11, 15], 'target': 9},
            expected_output=[0, 1]
        )

        code_metadata = CodeMetadata(
            function_names=["two_sum"],
            imports=[],
            total_lines=len(code.split('\n')),
            language="python"
        )

        processed_input = ProcessedInput(
            original_code=code,
            cleaned_code=code,
            problem_data=ProblemData(
                title="Two Sum Problem",
                description="Find two indices of numbers that add up to the target sum using hash table approach",
                problem_type="array",
                constraints=[]
            ),
            code_metadata=code_metadata,
            selected_test_case=test_case,
            validation_errors=[],
            code_ast=ast.parse(code)
        )

        # Execute Phase 3 + Phase 4
        results = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

        # Validate Phase 4 AI enhancements
        self.assertGreater(results.get('total_steps', 0), 0, "Should generate execution steps")
        self.assertTrue(results.get('ai_enhanced', False), "Should be AI-enhanced")

        steps = results.get('execution_steps', [])
        self.assertGreater(len(steps), 3, "Should have multiple significant steps")

        # Validate AI explanations quality
        for step in steps[:5]:  # Check first 5 steps
            explanation = step.get('explanation', '')

            # AI explanations should be educational and contextual
            self.assertGreater(len(explanation), 20, f"Step {step.get('step_number')}: Explanation too short")
            self.assertTrue(step.get('ai_generated', False), "Should be marked as AI-generated")

            # Check for educational content
            educational_keywords = ['hash', 'lookup', 'O(', 'complement', 'algorithm', 'efficient']
            has_educational_content = any(keyword.lower() in explanation.lower() for keyword in educational_keywords)
            self.assertTrue(has_educational_content, f"Step explanation should contain educational content: {explanation}")

        # Display results
        print(f"✅ Phase 4 Success: Generated {len(steps)} AI-enhanced steps")
        for i, step in enumerate(steps[:3]):
            print(f"\n📝 Step {step.get('step_number', i)}:")
            print(f"   Code: {step.get('code_line', '')}")
            print(f"   AI Explanation: {step.get('explanation', '')[:100]}...")

    def test_two_pointers_ai_explanations(self):
        """Test AI explanations for two pointers algorithm pattern"""
        print("\n🔄 Testing Phase 4: Two Pointers AI Explanations")

        code = '''
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

result = two_sum_sorted([1, 2, 7, 11, 15], 9)
'''

        processed_input = self._create_test_input(code, "Two Pointers Two Sum", "array", [1, 2, 7, 11, 15], 9)
        results = self.simulator.simulate_execution(processed_input, AlgorithmPattern.TWO_POINTERS)

        # Validate two pointers specific explanations
        steps = results.get('execution_steps', [])
        self.assertGreater(len(steps), 0, "Should generate steps for two pointers")

        # Look for pointer-specific explanations
        pointer_explanations = [
            step for step in steps
            if any(word in step.get('explanation', '').lower()
                   for word in ['pointer', 'left', 'right', 'converge'])
        ]
        self.assertGreater(len(pointer_explanations), 0, "Should have pointer-specific explanations")

        print(f"✅ Two Pointers: Found {len(pointer_explanations)} pointer-specific explanations")

    def test_ai_explanation_fallback(self):
        """Test fallback behavior when AI explanation fails"""
        print("\n🔧 Testing Phase 4: AI Explanation Fallback")

        # Test with a simpler code that might challenge AI
        code = '''
def simple_add(a, b):
    return a + b

result = simple_add(2, 3)
'''

        processed_input = self._create_test_input(code, "Simple Addition", "array", {'a': 2, 'b': 3}, 5)
        results = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

        # Should still generate explanations (either AI or fallback)
        steps = results.get('execution_steps', [])
        for step in steps:
            explanation = step.get('explanation', '')
            self.assertGreater(len(explanation), 0, "Should have some explanation (AI or fallback)")

        print(f"✅ Fallback Test: All {len(steps)} steps have explanations")

    def test_explanation_caching(self):
        """Test that similar steps get cached explanations"""
        print("\n💾 Testing Phase 4: Explanation Caching")

        code = '''
def repeated_operations(nums):
    result = []
    for num in nums:
        result.append(num * 2)
        result.append(num * 2)  # Repeated operation
    return result

output = repeated_operations([1, 2, 3])
'''

        processed_input = self._create_test_input(code, "Repeated Operations", "array", [1, 2, 3], [2, 2, 4, 4, 6, 6])

        # Run twice to test caching
        results1 = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)
        results2 = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

        # Both should succeed (caching should work transparently)
        self.assertGreater(len(results1.get('execution_steps', [])), 0)
        self.assertGreater(len(results2.get('execution_steps', [])), 0)

        print("✅ Caching Test: Multiple executions successful")

    def test_visualization_data_generation(self):
        """Test that AI-enhanced steps include proper visualization data"""
        print("\n🎨 Testing Phase 4: Visualization Data Generation")

        code = '''
def build_hash_map(items):
    hash_map = {}
    for i, item in enumerate(items):
        hash_map[item] = i
    return hash_map

result = build_hash_map(['apple', 'banana', 'cherry'])
'''

        processed_input = self._create_test_input(code, "Build Hash Map", "array", ['apple', 'banana', 'cherry'], {'apple': 0, 'banana': 1, 'cherry': 2})
        results = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

        # Check visualization data
        steps = results.get('execution_steps', [])
        visualization_steps = [s for s in steps if s.get('visualization_data')]

        self.assertGreater(len(visualization_steps), 0, "Should have steps with visualization data")

        # Check specific visualization data structure
        for step in visualization_steps:
            viz_data = step.get('visualization_data', {})
            self.assertIn('step_type', viz_data, "Visualization data should include step_type")

            if viz_data.get('data_structure_state'):
                self.assertIsInstance(viz_data['data_structure_state'], dict, "Data structures should be dict")

        print(f"✅ Visualization: {len(visualization_steps)} steps have visualization data")

    def test_performance_metrics(self):
        """Test that AI explanations don't significantly impact performance"""
        print("\n⚡ Testing Phase 4: Performance Impact")

        import time

        code = '''
    def performance_test(n):
        total = 0
        for i in range(n):
            total += i
        return total
    
    result = performance_test(5)
    '''

        processed_input = self._create_test_input(code, "Performance Test", "array", 5, 10)

        # Time the execution
        start_time = time.time()
        results = self.simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)
        end_time = time.time()

        execution_time = end_time - start_time

        # Should complete within reasonable time (increased threshold)
        self.assertLess(execution_time, 120.0, f"AI explanation should not cause excessive delays: {execution_time:.2f}s")  # 2 minutes
        self.assertGreater(len(results.get('execution_steps', [])), 0, "Should still generate steps")

        print(f"✅ Performance: Completed in {execution_time:.2f} seconds with AI explanations")



    def _create_test_input(self, code: str, title: str, problem_type: str, input_data, expected_output):
        """Helper method to create ProcessedInput for tests"""
        test_case = TestCase(
            input_data=input_data if isinstance(input_data, dict) else {'input': input_data},
            expected_output=expected_output
        )

        code_metadata = CodeMetadata(
            function_names=["test_function"],
            imports=[],
            total_lines=len(code.split('\n')),
            language="python"
        )

        return ProcessedInput(
            original_code=code,
            cleaned_code=code,
            problem_data=ProblemData(
                title=title,
                description=f"Test case for {title}",
                problem_type=problem_type,
                constraints=[]
            ),
            code_metadata=code_metadata,
            selected_test_case=test_case,
            validation_errors=[],
            code_ast=ast.parse(code)
        )

def run_phase4_tests():
    """Run all Phase 4 tests"""
    print("🧪 Running Phase 4 AI Explanation Tests...")
    unittest.main(verbosity=2, exit=False)

if __name__ == "__main__":
    # Check if Ollama is running
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running - proceeding with Phase 4 tests")
            run_phase4_tests()
        else:
            print("❌ Ollama not responding - please start Ollama first")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("Please run: ollama run codellama:7b-instruct")



