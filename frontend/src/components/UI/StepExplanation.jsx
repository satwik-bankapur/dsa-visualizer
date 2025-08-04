import React from 'react';

const StepExplanation = ({ step, stepNumber, totalSteps }) => {
    if (!step) return null;

    return (
        <div className="step-explanation">
            <h3>📖 Step {stepNumber} of {totalSteps}</h3>
            <p>{step.explanation || step.description}</p>

            {/* Add complexity info if available */}
            {step.complexity && (
                <div className="complexity-info">
                    <strong>Complexity:</strong> {step.complexity}
                </div>
            )}

            {/* Add code hint if available */}
            {step.codeHint && (
                <div className="code-hint">
                    <strong>Code:</strong> <code>{step.codeHint}</code>
                </div>
            )}
        </div>
    );
};

export default StepExplanation;
