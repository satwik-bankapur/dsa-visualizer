import React, { useState } from 'react';
import './CodeEditor.css';

const CodeEditor = ({ code, onChange, onVisualize, onClear, isAnalyzing }) => {
    const [customArray, setCustomArray] = useState('1,3,5,7,9,11');
    const [customTarget, setCustomTarget] = useState(7);

    const handleVisualize = () => {
        if (code.trim()) {
            onVisualize(code, customArray, customTarget);
        }
    };

    // Add this to your CodeEditor component
    const handleCustomVisualize = () => {
        const demoCode = `def binary_search(arr, target):
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

# Test with: [${customArray}], target = ${customTarget}`;

        onChange(demoCode);
        onVisualize(demoCode, customArray, customTarget);
    };


    return (
        <div className="code-editor">
            <h2>📝 Paste Your Code Here:</h2>

            <textarea
                value={code}
                onChange={(e) => onChange(e.target.value)}
                placeholder={`Paste your LeetCode solution here...

Example Binary Search:
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

# Test with: [1, 3, 5, 7, 9, 11], target = 7`}
                className="code-input"
                disabled={isAnalyzing}
            />

            <div className="button-group">
                <button
                    onClick={handleVisualize}
                    disabled={!code.trim() || isAnalyzing}
                    className="visualize-btn"
                >
                    {isAnalyzing ? '🔄 Analyzing...' : '🎯 Analyze & Visualize'}
                </button>

                <button
                    onClick={onClear}
                    disabled={isAnalyzing}
                    className="clear-btn"
                >
                    🗑️ Clear
                </button>
            </div>

            <div className="input-controls">
                <h3>🎮 Interactive Controls</h3>

                <div className="control-row">
                    <div className="input-group">
                        <label htmlFor="arrayInput">Custom Array:</label>
                        <input
                            id="arrayInput"
                            type="text"
                            value={customArray}
                            onChange={(e) => setCustomArray(e.target.value)}
                            placeholder="e.g., 1,3,5,7,9,11"
                            disabled={isAnalyzing}
                        />
                    </div>

                    <div className="input-group">
                        <label htmlFor="targetInput">Target Value:</label>
                        <input
                            id="targetInput"
                            type="number"
                            value={customTarget}
                            onChange={(e) => setCustomTarget(parseInt(e.target.value) || 0)}
                            placeholder="e.g., 7"
                            disabled={isAnalyzing}
                        />
                    </div>
                </div>

                <button
                    onClick={handleCustomVisualize}
                    disabled={isAnalyzing}
                    className="custom-visualize-btn"
                >
                    ▶️ Run with Custom Data
                </button>
            </div>
        </div>
    );
};

export default CodeEditor;
