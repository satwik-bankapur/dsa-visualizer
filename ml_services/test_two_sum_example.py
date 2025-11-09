# test_two_sum_example.py
import ast
from core.execution_simulator import ExecutionSimulator
from models.internal_models import (
    ProcessedInput, ProblemData, CodeMetadata, TestCase, AlgorithmPattern, Language, ProblemType
)

def test_two_sum_solution():
    """Test your Two Sum solution with AI-enhanced explanations"""

    # Your code (cleaned up for execution)
    code = '''
def twoSum(nums, target):
    numMap = {}
    n = len(nums)

    # Build the hash table
    for i in range(n):
        numMap[nums[i]] = i

    # Find the complement
    for i in range(n):
        complement = target - nums[i]
        if complement in numMap and numMap[complement] != i:
            return [i, numMap[complement]]

    return []

# Execute with test case
result = twoSum([2, 7, 11, 15], 9)
print(f"Result: {result}")
'''

    # Set up test case
    test_case = TestCase(
        input_data={"nums": [2, 7, 11, 15], "target": 9},
        expected_output=[0, 1]
    )

    # Create processed input
    processed_input = ProcessedInput(
        original_code=code,
        cleaned_code=code,
        problem_data=ProblemData(
            title="Two Sum - Hash Map Approach",
            description="Find two indices of numbers that add up to target using hash table with two passes",
            problem_type=ProblemType.ARRAY,
            constraints=[],
            test_cases=[test_case]
        ),
        code_metadata=CodeMetadata(
            language=Language.PYTHON,
            function_name="twoSum",
            parameters=["nums", "target"],
            lines_of_code=len(code.split('\n')),
            cyclomatic_complexity=2
        ),
        selected_test_case=test_case,
        validation_errors=[],
        code_ast=ast.parse(code)
    )

    # Run Phase 3 + 4 simulation
    simulator = ExecutionSimulator()
    results = simulator.simulate_execution(processed_input, AlgorithmPattern.HASH_MAP)

    # Display results
    print("=" * 80)
    print("🚀 TWO SUM EXECUTION ANALYSIS")
    print("=" * 80)

    print(f"\n📊 SUMMARY:")
    print(f"   • Total Steps Generated: {results.get('total_steps', 0)}")
    print(f"   • AI Enhanced: {results.get('ai_enhanced', False)}")
    print(f"   • Algorithm Pattern: {results.get('algorithm_pattern', 'Unknown')}")
    print(f"   • Test Case: nums={test_case.input_data['nums']}, target={test_case.input_data['target']}")

    # Display step-by-step execution
    steps = results.get('execution_steps', [])

    print(f"\n🔍 STEP-BY-STEP EXECUTION TRACE:")
    print("-" * 80)

    for i, step in enumerate(steps):
        print(f"\n📝 STEP {step.get('step_number', i+1)}:")
        print(f"   📄 Code: {step.get('code_line', '').strip()}")
        print(f"   🎯 Function: {step.get('function_name', 'main')}")
        print(f"   🔄 Event: {step.get('event_type', 'unknown')}")

        # Show variable changes
        var_changes = step.get('variable_changes', {})
        if var_changes:
            print(f"   📊 Variable Changes:")
            for var, change in var_changes.items():
                if change.get('type') == 'new':
                    print(f"      ✨ {var} = {change['new']}")
                elif change.get('type') == 'modified':
                    print(f"      🔄 {var}: {change['old']} → {change['new']}")

        # Show AI explanation
        explanation = step.get('explanation', '')
        if explanation:
            print(f"   🧠 AI Explanation:")
            print(f"      {explanation}")

        # Show visualization data
        viz_data = step.get('visualization_data', {})
        if viz_data.get('data_structure_state'):
            print(f"   🎨 Data Structures:")
            for name, state in viz_data['data_structure_state'].items():
                if state['type'] == 'hash_map':
                    print(f"      📊 {name}: {state['entries']} (size: {state['size']})")
                elif state['type'] == 'array':
                    print(f"      📋 {name}: {state['values']}")

        print("-" * 40)

    # Display execution summary
    summary = results.get('execution_summary', {})
    if summary:
        print(f"\n📈 EXECUTION SUMMARY:")
        print(f"   • Operation Counts: {summary.get('operation_counts', {})}")
        print(f"   • Key Operations: {summary.get('key_operations', [])}")
        print(f"   • Performance Notes: {summary.get('performance_notes', [])}")
        if summary.get('complexity_analysis'):
            complexity = summary['complexity_analysis']
            print(f"   • Time Complexity: {complexity.get('time', 'Unknown')}")
            print(f"   • Space Complexity: {complexity.get('space', 'Unknown')}")

if __name__ == "__main__":
    print("🧪 Testing Two Sum Solution with AI-Enhanced Step Analysis")
    print("🔄 This will take 1-3 minutes to generate AI explanations...")
    test_two_sum_solution()
