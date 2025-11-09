# 🚀 DSA Visualizer - AI-Powered Algorithm Visualization

An intelligent platform that analyzes your code, detects algorithm patterns, and provides step-by-step visualizations with AI-enhanced explanations.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Automatic algorithm pattern detection
- 📊 **Interactive Visualization**: Step-by-step algorithm execution
- 🧠 **Smart Explanations**: AI-generated educational explanations
- 🔄 **Real-time Processing**: Instant code analysis and visualization
- 🛡️ **Robust Architecture**: Fallback mechanisms for reliability
- 🎯 **Multi-Algorithm Support**: Binary Search, Two Pointers, Hash Maps, and more

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │  ML Services    │
│   (React)       │◄──►│   (FastAPI)     │
│   Port 3000     │    │   Port 8001     │
└─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- npm or yarn

### Installation & Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd dsa-visualizer
```

2. **Install ML Services dependencies**
```bash
cd ml_services
pip install -r requirements.txt
cd ..
```


3**Install Frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

4**Start all services (Windows)**
```bash
start-all-services.bat
```

**Or start manually:**
```bash
# Terminal 1: ML Services
cd ml_services && python main.py

# Terminal 2: Frontend  
cd frontend && npm start
```

6. **Verify integration**
```bash
python test-integration.py
```

7. **Open your browser**
Navigate to `http://localhost:3000`

## 🎯 Usage

1. **Paste your algorithm code** in the code editor
2. **Customize input data** (optional)
3. **Click "Analyze & Visualize"**
4. **Watch the step-by-step execution** with AI explanations
5. **Use playback controls** to navigate through steps

### Example Code
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 🧠 Supported Algorithms

- **Binary Search** - O(log n) search in sorted arrays
- **Two Pointers** - Efficient array traversal technique  
- **Sliding Window** - Optimal subarray/substring problems
- **Hash Map** - O(1) lookup-based solutions
- **Tree Traversal** - DFS/BFS tree algorithms
- **Dynamic Programming** - Optimal substructure problems
- **Greedy Algorithms** - Local optimization strategies

## 🔧 Configuration

### ML Services Configuration
Edit `ml_services/config/settings.py`:
```python
LOG_LEVEL = "INFO"
PORT = 8001
MODEL_NAME = "codellama:7b-instruct"  # Ollama model
```


## 🛡️ Fallback Mechanisms

The system includes multiple fallback layers:

1. **ML Service Down**: Frontend falls back to local algorithm detection
2. **AI Explanations Fail**: Uses rule-based explanations
3. **Code Tracing Fails**: Uses AST-based step generation
4. **Network Issues**: Graceful error handling with user feedback

## 🧪 Testing

### Integration Tests
```bash
python test-integration.py
```

### Individual Service Tests
```bash
# ML Services
cd ml_services && python -m pytest tests/

# Frontend  
cd frontend && npm test
```

## 📊 API Endpoints

### ML Services (Port 8001)
- `GET /health` - Health check
- `POST /api/analyze` - Unified analysis endpoint
- `POST /analysis/` - Detailed analysis with phases
- `GET /analysis/patterns` - Supported patterns


## 🔍 Troubleshooting

### Common Issues

**ML Service won't start:**
```bash
cd ml_services
pip install -r requirements.txt
python main.py
```

**Frontend shows "ML Service Offline":**
- Check if ML service is running on port 8001
- Verify no firewall blocking the connection
- Check `ml_services/logs/ml_service.log` for errors

**Analysis fails:**
- Ensure code is syntactically correct
- Check that the algorithm is supported
- Verify input data format

**Ollama not available:**
- The system will automatically use fallback explanations
- To enable AI explanations, install Ollama and the required model

### Logs
- ML Services: `ml_services/logs/ml_service.log`
- Backend: Console output
- Frontend: Browser developer console

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with React and FastAPI
- AI explanations powered by Ollama
- Algorithm visualizations inspired by educational needs

---

**Ready to visualize algorithms like never before?** 🚀

Open `http://localhost:3000` and start exploring!