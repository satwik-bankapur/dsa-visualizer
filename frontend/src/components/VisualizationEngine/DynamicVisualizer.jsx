// components/VisualizationEngine/DynamicVisualizer.jsx
import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ArrayVisualizer from './ArrayVisualizer';
import HashMapVisualizer from './HashMapVisualizer';
import TreeVisualizer from './TreeVisualizer';
import './DynamicVisualizer.css';

const DynamicVisualizer = ({ algorithmType, currentStep, executionSteps }) => {
    // Memoize the current step data to prevent unnecessary re-renders
    const currentStepData = useMemo(() => {
        if (!executionSteps || !executionSteps[currentStep]) {
            return {
                explanation: 'No step data available',
                visualizationData: {
                    dataStructures: {},
                    highlights: [],
                    pointers: {},
                    activeElements: []
                }
            };
        }
        return executionSteps[currentStep];
    }, [executionSteps, currentStep]);

    // Select the appropriate visualizer component
    const getVisualizerComponent = (algorithmType) => {
        switch (algorithmType) {
            case 'TWO_POINTERS':
            case 'BINARY_SEARCH':
            case 'SLIDING_WINDOW':
                return ArrayVisualizer;
            case 'HASH_MAP':
                return HashMapVisualizer;
            case 'DEPTH_FIRST_SEARCH':
            case 'BREADTH_FIRST_SEARCH':
            case 'TREE_TRAVERSAL':
                return TreeVisualizer;
            default:
                return ArrayVisualizer;
        }
    };

    const VisualizerComponent = getVisualizerComponent(algorithmType);

    if (!executionSteps || executionSteps.length === 0) {
        return (
            <div className="dynamic-visualizer">
                <div className="no-visualization">
                    <div className="placeholder-icon">📊</div>
                    <p>Visualization will appear here after analysis</p>
                </div>
            </div>
        );
    }

    return (
        <div className="dynamic-visualizer">
            <div className="visualizer-header">
                <div className="algorithm-badge">
                    <span className="algorithm-icon">🧠</span>
                    <span className="algorithm-name">
            {algorithmType?.replace(/_/g, ' ') || 'Unknown Algorithm'}
          </span>
                </div>
                <div className="step-indicator">
                    <span>Step {currentStep + 1}</span>
                </div>
            </div>

            <div className="visualizer-content">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={`step-${currentStep}-${algorithmType}`}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{
                            duration: 0.4,
                            ease: "easeInOut"
                        }}
                    >
                        <VisualizerComponent
                            data={currentStepData.visualizationData?.dataStructures || {}}
                            highlights={currentStepData.visualizationData?.highlights || []}
                            pointers={currentStepData.visualizationData?.pointers || {}}
                            activeElements={currentStepData.visualizationData?.activeElements || []}
                            algorithmType={algorithmType}
                            stepNumber={currentStep}
                        />
                    </motion.div>
                </AnimatePresence>
            </div>

            <motion.div
                className="step-explanation"
                key={`explanation-${currentStep}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.2 }}
            >
                <div className="explanation-content">
                    <span className="explanation-icon">💡</span>
                    <p>{currentStepData.explanation || 'No explanation available for this step'}</p>
                </div>

                {currentStepData.codeLine && (
                    <div className="code-line">
                        <span className="code-label">Code:</span>
                        <code>{currentStepData.codeLine}</code>
                    </div>
                )}
            </motion.div>
        </div>
    );
};

export default DynamicVisualizer;
