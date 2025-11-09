// App.js
import React, { useState, useEffect, useRef } from 'react';
import CodeEditor from './components/CodeEditor/CodeEditor';
import DynamicVisualizer from './components/VisualizationEngine/DynamicVisualizer';
import PlaybackControls from './components/Controls/PlaybackControls';
import mlApiService from './services/mlApiService';
import './App.css';

function App() {
  // State management for the entire app
  const [code, setCode] = useState(`def twoSum(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []`);

  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000);
  const [serviceStatus, setServiceStatus] = useState('checking');

  const timerRef = useRef(null);

  // Auto-play functionality
  useEffect(() => {
    if (isPlaying && analysis?.executionSteps?.length) {
      timerRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= analysis.executionSteps.length - 1) {
            clearInterval(timerRef.current);
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    } else {
      clearInterval(timerRef.current);
    }

    return () => clearInterval(timerRef.current);
  }, [isPlaying, analysis, speed]);

  // Check ML service status on mount
  useEffect(() => {
    checkServiceHealth();
  }, []);

  const checkServiceHealth = async () => {
    try {
      setServiceStatus('checking');
      const isHealthy = await mlApiService.checkHealth();
      setServiceStatus(isHealthy ? 'connected' : 'disconnected');
    } catch (error) {
      setServiceStatus('disconnected');
    }
  };

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysis(null);

    try {
      const result = await mlApiService.analyzeCode(code);
      setAnalysis(result);
      setCurrentStep(0);
      setIsPlaying(false);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleStepChange = (direction) => {
    if (!analysis?.executionSteps?.length) return;

    setCurrentStep((prev) => {
      const newStep = prev + direction;
      return Math.max(0, Math.min(analysis.executionSteps.length - 1, newStep));
    });
  };

  const handlePlay = () => setIsPlaying(true);
  const handlePause = () => setIsPlaying(false);

  const handleReset = () => {
    setCurrentStep(0);
    setIsPlaying(false);
  };

  const handleSpeedChange = (newSpeed) => {
    setSpeed(newSpeed);
  };

  return (
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <div className="title-section">
              <h1>🧠 Smart DSA Visualizer</h1>
              <p>AI-Powered Algorithm Analysis & Visualization</p>
            </div>
            <div className={`service-status ${serviceStatus}`}>
              <div className="status-indicator"></div>
              <span>ML Service: {serviceStatus}</span>
            </div>
          </div>
        </header>

        <main className="app-main">
          <section className="editor-section">
            <div className="section-header">
              <h2>Algorithm Code</h2>
              <button
                  className={`analyze-button ${isAnalyzing ? 'analyzing' : ''}`}
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
              >
                {isAnalyzing ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing...
                    </>
                ) : (
                    <>
                      <span>🔍</span>
                      Analyze Code
                    </>
                )}
              </button>
            </div>

            <CodeEditor
                value={code}
                onChange={setCode}
                placeholder="Write your algorithm code here..."
            />
          </section>

          <section className="visualization-section">
            {error && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  <p>{error}</p>
                  <button onClick={() => setError(null)} className="dismiss-error">✕</button>
                </div>
            )}

            {analysis && (
                <div className="analysis-container">
                  <div className="analysis-header">
                    <div className="algorithm-info">
                      <h3>{analysis.algorithm.name}</h3>
                      <div className="metrics">
                    <span className="confidence">
                      {Math.round(analysis.algorithm.confidence * 100)}% confidence
                    </span>
                        <span className="complexity">
                      Time: {analysis.complexity.time} | Space: {analysis.complexity.space}
                    </span>
                      </div>
                    </div>
                  </div>

                  <PlaybackControls
                      isPlaying={isPlaying}
                      currentStep={currentStep}
                      totalSteps={analysis.executionSteps.length}
                      speed={speed}
                      onPlay={handlePlay}
                      onPause={handlePause}
                      onStep={handleStepChange}
                      onReset={handleReset}
                      onSpeedChange={handleSpeedChange}
                  />

                  <DynamicVisualizer
                      algorithmType={analysis.algorithm.type}
                      currentStep={currentStep}
                      executionSteps={analysis.executionSteps}
                  />
                </div>
            )}

            {!analysis && !error && !isAnalyzing && (
                <div className="empty-state">
                  <div className="empty-icon">📊</div>
                  <h3>Ready to Visualize!</h3>
                  <p>Write your algorithm code and click "Analyze" to see the magic happen</p>
                </div>
            )}
          </section>
        </main>
      </div>
  );
}

export default App;
