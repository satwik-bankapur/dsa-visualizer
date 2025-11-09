import requests
import json

# Test the ML service with the correct format
url = "http://localhost:8001/api/analyze"
test_code = """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1"""

data = {
    "code": test_code,
    "language": "python",
    "problem_description": "Algorithm visualization and analysis",
    "input_data": {
        "nums": [1, 3, 5, 7, 9, 11],
        "target": 7
    }
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"Algorithm: {result.get('algorithm_analysis', {}).get('primary_pattern')}")
        print(f"Steps: {len(result.get('algorithm_analysis', {}).get('execution_steps', []))}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")