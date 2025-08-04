import React from 'react';

const AlgorithmInfo = ({ algorithm, parsedData }) => {
    const getAlgorithmDescription = (algo) => {
        const descriptions = {
            'Binary Search': 'Efficiently searches sorted arrays by repeatedly dividing the search space in half. Time: O(log n), Space: O(1)',
            'Two Pointers': 'Uses two pointers moving towards each other to solve problems efficiently. Time: O(n), Space: O(1)',
            'Sliding Window': 'Maintains a window that slides through the array to find optimal solutions. Time: O(n), Space: O(1)',
            'Sorting Algorithm': 'Arranges elements in a specific order. Time complexity varies by algorithm.',
            'Unknown Algorithm': 'Try: Binary Search, Two Pointers, Sliding Window, or Sorting algorithms'
        };
        return descriptions[algo] || 'Algorithm not recognized.';
    };

    return (
        <div className="algorithm-info">
            <h3>🎯 Detected: {algorithm}</h3>
            <p>{getAlgorithmDescription(algorithm)}</p>
            {parsedData && parsedData.arrays.length > 0 && (
                <p><strong>Array:</strong> [{parsedData.arrays[0].join(', ')}]</p>
            )}
            {parsedData && parsedData.target && (
                <p><strong>Target:</strong> {parsedData.target}</p>
            )}
        </div>
    );
};

export default AlgorithmInfo;
