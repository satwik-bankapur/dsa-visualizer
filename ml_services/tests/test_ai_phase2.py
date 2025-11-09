# test_ai_phase2.py
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now your imports will work
from ml_services.core.ai_pattern_matcher import AIPatternMatcher
from ml_services.data.training_data_builder import TrainingDataBuilder
import ast
def test_ai_pattern_matcher():
    print("🤖 Testing AI Pattern Matcher")

    # Build training data
    builder = TrainingDataBuilder()
    training_data = builder.add_samples()
    print(f"Training samples: {len(training_data)}")

    # Train model
    matcher = AIPatternMatcher()
    metrics = matcher.train(training_data)
    print(f"Training metrics: {metrics}")

    # Test predictions
    test_code = """
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
"""

    tree = ast.parse(test_code)
    pattern, confidence = matcher.predict_pattern(tree, test_code)
    print(f"Predicted: {pattern} (confidence: {confidence:.3f})")

    # Feature importance
    importances = matcher.get_feature_importance()
    top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 important features:")
    for feature, importance in top_features:
        print(f"  {feature}: {importance:.3f}")

if __name__ == "__main__":
    test_ai_pattern_matcher()
