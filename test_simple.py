import requests
import json

url = "http://localhost:8001/api/analyze"
data = {
    "code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    return left",
    "language": "python",
    "input_data": {"nums": [1, 3, 5], "target": 3}
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")