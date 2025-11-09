import requests
import json

url = "http://localhost:8001/api/analyze"
data = {
    "code": "def twoSum(nums, target):\n    left, right = 0, len(nums) - 1\n    return left",
    "language": "python",
    "input_data": {"nums": [2, 7, 11, 15], "target": 9}
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")