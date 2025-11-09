# Simple main.py without complex dependencies
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class SimpleMLHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "service": "ml_services"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                code = request_data.get('code', '')
                
                # Simple algorithm detection
                algorithm = self.detect_algorithm(code)
                steps = self.generate_steps(algorithm, request_data)
                
                response = {
                    "status": "success",
                    "algorithm_analysis": {
                        "primary_pattern": algorithm.upper().replace(' ', '_'),
                        "confidence_score": 0.8,
                        "execution_steps": steps,
                        "complexity_analysis": {
                            "time": "O(log n)" if "Binary" in algorithm else "O(n)",
                            "space": "O(1)"
                        }
                    },
                    "processing_time": 0.1
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def detect_algorithm(self, code):
        code_lower = code.lower()
        if 'left' in code_lower and 'right' in code_lower and 'mid' in code_lower:
            return 'Binary Search'
        elif 'left' in code_lower and 'right' in code_lower:
            return 'Two Pointers'
        elif 'hash' in code_lower or 'dict' in code_lower or '{}' in code:
            return 'Hash Map'
        return 'Unknown Algorithm'

    def generate_steps(self, algorithm, request_data):
        # Extract input data from request
        input_data = request_data.get('input_data', {})
        array = input_data.get('nums', [1, 3, 5, 7, 9, 11])
        target = input_data.get('target', 7)
        
        if algorithm == 'Binary Search':
            return self.generate_binary_search_steps(array, target)
        elif algorithm == 'Two Pointers':
            return self.generate_two_pointers_steps(array, target)
        
        return [{
            "step_number": 1,
            "code_line": "Algorithm detected",
            "explanation": f"Analyzing {algorithm} implementation...",
            "variables_after": {"nums": array, "target": target},
            "variable_changes": {}
        }]

    def generate_binary_search_steps(self, array, target):
        steps = []
        left, right = 0, len(array) - 1
        step_num = 0
        
        steps.append({
            "step_number": step_num,
            "code_line": "left, right = 0, len(arr) - 1",
            "explanation": f"Initialize: left={left}, right={right}",
            "variables_after": {"arr": array, "target": target, "left": left, "right": right},
            "variable_changes": {"left": left, "right": right}
        })
        
        step_num += 1
        while left <= right and step_num < 10:
            mid = (left + right) // 2
            
            steps.append({
                "step_number": step_num,
                "code_line": f"mid = (left + right) // 2",
                "explanation": f"Calculate mid = ({left} + {right}) // 2 = {mid}",
                "variables_after": {"arr": array, "target": target, "left": left, "right": right, "mid": mid},
                "variable_changes": {"mid": mid}
            })
            
            step_num += 1
            if array[mid] == target:
                steps.append({
                    "step_number": step_num,
                    "code_line": "return mid",
                    "explanation": f"Found! arr[{mid}] = {array[mid]} equals target {target}",
                    "variables_after": {"arr": array, "target": target, "left": left, "right": right, "mid": mid},
                    "variable_changes": {}
                })
                break
            elif array[mid] < target:
                left = mid + 1
                steps.append({
                    "step_number": step_num,
                    "code_line": "left = mid + 1",
                    "explanation": f"arr[{mid}] = {array[mid]} < {target}, search right half",
                    "variables_after": {"arr": array, "target": target, "left": left, "right": right, "mid": mid},
                    "variable_changes": {"left": left}
                })
            else:
                right = mid - 1
                steps.append({
                    "step_number": step_num,
                    "code_line": "right = mid - 1",
                    "explanation": f"arr[{mid}] = {array[mid]} > {target}, search left half",
                    "variables_after": {"arr": array, "target": target, "left": left, "right": right, "mid": mid},
                    "variable_changes": {"right": right}
                })
            step_num += 1
        
        return steps

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8001), SimpleMLHandler)
    print("Simple ML Service running on http://localhost:8001")
    print("Health check: http://localhost:8001/health")
    server.serve_forever()