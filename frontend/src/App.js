import React, { useState } from 'react';
import CodeEditor from './components/CodeEditor/CodeEditor';
import AlgorithmVisualizer from './components/Visualizer/AlgorithmVisualizer';
import AlgorithmInfo from './components/UI/AlgorithmInfo';
import StepExplanation from './components/UI/StepExplanation';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [algorithm, setAlgorithm] = useState(null);
  const [steps, setSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [parsedData, setParsedData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleVisualize = async (codeInput, customArray = null, customTarget = null) => {
    setIsAnalyzing(true);

    try {
      // Import your converted services
      const { parseCodeInput } = await import('./utils/codeParser');
      const { detectAlgorithm } = await import('./services/algorithmDetector');
      const { generateVisualizationSteps } = await import('./services/visualizationGenerator');

      // Parse the code
      const parsed = parseCodeInput(codeInput, customArray, customTarget);
      const detectedAlg = detectAlgorithm(codeInput);
      const generatedSteps = generateVisualizationSteps(detectedAlg, parsed);

      setParsedData(parsed);
      setAlgorithm(detectedAlg);
      setSteps(generatedSteps);
      setCurrentStep(0);
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setAlgorithm(null);
    setSteps([]);
    setCurrentStep(0);
    setParsedData(null);
  };

  return (
      <div className="App">
        <div className="container">
          <h1>🚀 DSA Code Visualizer</h1>

          <div className="main-content">
            <div className="input-section">
              <CodeEditor
                  code={code}
                  onChange={setCode}
                  onVisualize={handleVisualize}
                  onClear={handleClear}
                  isAnalyzing={isAnalyzing}
              />

              {algorithm && (
                  <AlgorithmInfo
                      algorithm={algorithm}
                      parsedData={parsedData}
                  />
              )}
            </div>

            <div className="output-section">
              <AlgorithmVisualizer
                  algorithm={algorithm}
                  steps={steps}
                  currentStep={currentStep}
                  onStepChange={setCurrentStep}
              />

              {steps.length > 0 && (
                  <StepExplanation
                      step={steps[currentStep]}
                      stepNumber={currentStep + 1}
                      totalSteps={steps.length}
                  />
              )}
            </div>
          </div>
        </div>
      </div>
  );
}

export default App;
