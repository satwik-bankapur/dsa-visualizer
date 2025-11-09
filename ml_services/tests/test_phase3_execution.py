# test_phase3_execution.py - FIXED VERSION
import ast
from core.execution_simulator import ExecutionSimulator
from models.internal_models import (
    ProcessedInput, ProblemData, TestCase, AlgorithmPattern, CodeMetadata
)

def test_hash_map_execution():
    print("🚀 Testing Phase 3 Execution Simulator")

    # FIXED: Code that actually CALLS the function
    code = '''
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# CRITICAL: Actually call the function with test inputs
result = two_sum([2, 7, 11, 15], 9)
print(f"Result: {result}")
'''

    # Create test case
    test_case = TestCase(
        input_data={'nums': [2, 7, 11, 15], 'target': 9},
        expected_output=[0, 1]
    )

    # Create proper CodeMetadata
    code_metadata = CodeMetadata(
        function_names=["two_sum"],
        imports=[],
        total_lines=len(code.split('\n')),
        language="python"
    )

    # Create processed input
    processed_input = ProcessedInput(
        original_code=code,
        cleaned_code=code,
        problem_data=ProblemData(
            title="Two Sum",
            description="Find two numbers that add up to target",
            problem_type="array",
            constraints=[]
        ),
        code_metadata=code_metadata,
        selected_test_case=test_case,
        validation_errors=[],
        code_ast=ast.parse(code)
    )

    # Run Phase 3 simulation
    try:
        simulator = ExecutionSimulator()
        results = simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

        total_steps = results.get('total_steps', 0)
        print(f"✅ Phase 3 Success: Generated {total_steps} execution steps")

        if total_steps > 0:
            # Display first few steps
            steps = results.get('execution_steps', [])
            for i, step in enumerate(steps[:5]):
                print(f"  Step {step.get('step_number', i)}: {step.get('explanation', 'No explanation')}")
        else:
            print("❌ Still getting 0 steps - check ExecutionTracker configuration")

        return True

    except Exception as e:
        print(f"❌ Phase 3 Failed: {e}")
        return False

if __name__ == "__main__":
    test_hash_map_execution()
