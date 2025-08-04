import React from 'react';

const ArrayVisualizer = ({ algorithm, stepData }) => {
    if (!stepData) return null;

    const renderArrayElement = (value, index) => {
        let className = 'array-element';

        // Apply different styles based on the step data
        if (stepData.found && index === stepData.mid) {
            className += ' found';
        } else if (index === stepData.left) {
            className += ' left-pointer';
        } else if (index === stepData.right) {
            className += ' right-pointer';
        } else if (index === stepData.mid) {
            className += ' mid-pointer';
        } else if (stepData.left !== undefined && stepData.right !== undefined &&
            (index < stepData.left || index > stepData.right)) {
            className += ' eliminated';
        }

        return (
            <div key={index} className={className}>
                <div className="index-label">{index}</div>
                <div className="value">{value}</div>
            </div>
        );
    };

    const renderLegend = () => {
        const legendItems = [];

        if (stepData.left !== undefined) {
            legendItems.push(
                <span key="left" className="legend-item left">
          Left: {stepData.left}
        </span>
            );
        }

        if (stepData.right !== undefined) {
            legendItems.push(
                <span key="right" className="legend-item right">
          Right: {stepData.right}
        </span>
            );
        }

        if (stepData.mid !== undefined && stepData.mid !== null) {
            legendItems.push(
                <span key="mid" className="legend-item mid">
          Mid: {stepData.mid}
        </span>
            );
        }

        if (stepData.sum !== undefined) {
            legendItems.push(
                <span key="sum" className="legend-item sum">
          Sum: {stepData.sum}
        </span>
            );
        }

        return legendItems;
    };

    return (
        <div className="array-visualizer">
            <div className="algorithm-header">
                <h3>{getAlgorithmIcon(algorithm)} {algorithm} Visualization</h3>
                <p>
                    <strong>Target:</strong> {stepData.target} |
                    <strong> Array:</strong> [{stepData.array.join(', ')}]
                </p>
            </div>

            <div className="array-container">
                <div className="array-visualization">
                    {stepData.array.map((value, index) => renderArrayElement(value, index))}
                </div>

                <div className="pointers-legend">
                    {renderLegend()}
                </div>
            </div>

            <div className="current-step">
                <strong>Current Action:</strong> {stepData.description}
            </div>
        </div>
    );
};

const getAlgorithmIcon = (algorithm) => {
    const icons = {
        'Binary Search': '🔍',
        'Two Pointers': '👆',
        'Sorting Algorithm': '🔄',
        'Sliding Window': '🪟'
    };
    return icons[algorithm] || '📊';
};

export default ArrayVisualizer;
