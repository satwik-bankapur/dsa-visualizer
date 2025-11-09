// components/VisualizationEngine/ArrayVisualizer.jsx
import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import './ArrayVisualizer.css';

const ArrayVisualizer = ({
                             data,
                             highlights = [],
                             pointers = {},
                             algorithmType,
                             stepNumber
                         }) => {
    // Extract array data from different possible structures
    const arrayData = useMemo(() => {
        if (data.nums?.values) return data.nums.values;
        if (data.array?.values) return data.array.values;
        if (data.arr?.values) return data.arr.values;
        if (Array.isArray(data.nums)) return data.nums;
        if (Array.isArray(data.array)) return data.array;
        if (Array.isArray(data.arr)) return data.arr;
        return [2, 7, 11, 15]; // Default example array
    }, [data]);

    // Generate element styles based on algorithm and state
    const getElementStyle = (index, value) => {
        let className = 'array-element';

        // Highlight active indices
        if (highlights.includes(index)) {
            className += ' highlighted';
        }

        // Algorithm-specific pointer styling
        switch (algorithmType) {
            case 'TWO_POINTERS':
                if (pointers.left === index) className += ' left-pointer';
                if (pointers.right === index) className += ' right-pointer';
                if (pointers.left === index && pointers.right === index) {
                    className += ' overlapping-pointers';
                }
                break;

            case 'BINARY_SEARCH':
                if (pointers.mid === index) className += ' mid-pointer';
                const low = pointers.low ?? pointers.left ?? 0;
                const high = pointers.high ?? pointers.right ?? arrayData.length - 1;
                if (index >= low && index <= high) {
                    className += ' search-range';
                }
                if (index < low || index > high) {
                    className += ' out-of-range';
                }
                break;

            case 'SLIDING_WINDOW':
                const start = pointers.start ?? pointers.left ?? 0;
                const end = pointers.end ?? pointers.right ?? 0;
                if (index >= start && index <= end) {
                    className += ' in-window';
                }
                if (pointers.windowStart === index) className += ' window-start';
                if (pointers.windowEnd === index) className += ' window-end';
                break;
        }

        return className;
    };

    // Render pointer labels
    const renderPointerLabels = () => {
        if (Object.keys(pointers).length === 0) return null;

        return (
            <div className="pointer-labels">
                {Object.entries(pointers).map(([name, position]) => {
                    if (position < 0 || position >= arrayData.length) return null;

                    return (
                        <motion.div
                            key={name}
                            className={`pointer-label ${name}-label`}
                            initial={{ opacity: 0, y: -10 }}
                            animate={{
                                opacity: 1,
                                y: 0,
                                x: position * 70 // 70px per element
                            }}
                            transition={{
                                type: "spring",
                                stiffness: 300,
                                damping: 30
                            }}
                        >
                            <span className="label-text">{name}</span>
                            <div className="label-arrow">↓</div>
                        </motion.div>
                    );
                })}
            </div>
        );
    };

    // Render search range indicator for binary search
    const renderSearchRange = () => {
        if (algorithmType !== 'BINARY_SEARCH' || !pointers.low !== undefined || !pointers.high !== undefined) {
            return null;
        }

        const low = pointers.low ?? pointers.left ?? 0;
        const high = pointers.high ?? pointers.right ?? arrayData.length - 1;

        return (
            <motion.div
                className="search-range-indicator"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                style={{
                    left: `${low * 70}px`,
                    width: `${(high - low + 1) * 70}px`
                }}
            />
        );
    };

    return (
        <div className="array-visualizer">
            <div className="array-container">
                {renderSearchRange()}

                <div className="array-elements">
                    {arrayData.map((value, index) => (
                        <motion.div
                            key={`${stepNumber}-${index}`}
                            className={getElementStyle(index, value)}
                            initial={{ scale: 0.8, opacity: 0, y: 20 }}
                            animate={{
                                scale: highlights.includes(index) ? 1.1 : 1,
                                opacity: 1,
                                y: 0
                            }}
                            transition={{
                                duration: 0.4,
                                delay: index * 0.05, // Stagger animation
                                type: "spring",
                                stiffness: 300
                            }}
                            whileHover={{ scale: 1.05 }}
                        >
                            <div className="element-value">{value}</div>
                            <div className="element-index">{index}</div>
                        </motion.div>
                    ))}
                </div>

                {renderPointerLabels()}
            </div>

            {/* Variables Display */}
            {Object.keys(pointers).length > 0 && (
                <motion.div
                    className="variables-display"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <h4>Current Variables:</h4>
                    <div className="variables-list">
                        {Object.entries(pointers).map(([name, value]) => (
                            <div key={name} className="variable-item">
                                <span className="var-name">{name}:</span>
                                <motion.span
                                    className="var-value"
                                    key={`${name}-${value}`}
                                    initial={{ scale: 1.2, color: '#3b82f6' }}
                                    animate={{ scale: 1, color: '#1f2937' }}
                                    transition={{ duration: 0.3 }}
                                >
                                    {value}
                                </motion.span>
                            </div>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Algorithm-specific info */}
            {algorithmType === 'TWO_POINTERS' && (
                <div className="algorithm-info">
                    <p>🔍 Searching with two pointers moving toward each other</p>
                </div>
            )}

            {algorithmType === 'BINARY_SEARCH' && (
                <div className="algorithm-info">
                    <p>🎯 Dividing search space in half each iteration</p>
                </div>
            )}

            {algorithmType === 'SLIDING_WINDOW' && (
                <div className="algorithm-info">
                    <p>🪟 Maintaining a sliding window over the array</p>
                </div>
            )}
        </div>
    );
};

export default ArrayVisualizer;
