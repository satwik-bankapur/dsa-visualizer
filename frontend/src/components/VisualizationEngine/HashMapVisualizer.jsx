// components/VisualizationEngine/HashMapVisualizer.jsx
import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './HashMapVisualizer.css';

const HashMapVisualizer = ({
                               data,
                               highlights = [],
                               pointers = {},
                               activeElements = [],
                               algorithmType
                           }) => {
    // Extract data structures
    const hashMap = useMemo(() => {
        if (data.numMap?.entries) return data.numMap.entries;
        if (data.map?.entries) return data.map.entries;
        if (data.hashMap?.entries) return data.hashMap.entries;
        return {};
    }, [data]);

    const array = useMemo(() => {
        if (data.nums?.values) return data.nums.values;
        if (data.array?.values) return data.array.values;
        if (data.arr?.values) return data.arr.values;
        return [2, 7, 11, 15]; // Default example
    }, [data]);

    // Get current operation info
    const currentOperation = useMemo(() => {
        return {
            complement: pointers.complement,
            target: pointers.target,
            currentValue: pointers.i !== undefined ? array[pointers.i] : undefined,
            currentIndex: pointers.i
        };
    }, [pointers, array]);

    return (
        <div className="hashmap-visualizer">
            <div className="visualization-grid">
                {/* Original Array Section */}
                <div className="array-section">
                    <div className="section-header">
                        <h4>📊 Original Array</h4>
                        <span className="section-subtitle">Input data</span>
                    </div>

                    <div className="array-elements">
                        {array.map((value, index) => (
                            <motion.div
                                key={index}
                                className={`array-element ${
                                    highlights.includes(index) ? 'highlighted' : ''
                                } ${pointers.i === index ? 'current' : ''}`}
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{
                                    scale: highlights.includes(index) ? 1.15 : 1,
                                    opacity: 1
                                }}
                                transition={{ duration: 0.3, delay: index * 0.05 }}
                            >
                                <div className="element-value">{value}</div>
                                <div className="element-index">{index}</div>
                                {pointers.i === index && (
                                    <motion.div
                                        className="current-indicator"
                                        initial={{ opacity: 0, y: -10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                    >
                                        👆
                                    </motion.div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Hash Map Section */}
                <div className="hashmap-section">
                    <div className="section-header">
                        <h4>🗂️ Hash Map</h4>
                        <span className="section-subtitle">
              {Object.keys(hashMap).length} entries
            </span>
                    </div>

                    <div className="hashmap-container">
                        {Object.keys(hashMap).length === 0 ? (
                            <div className="empty-hashmap">
                                <div className="empty-icon">📦</div>
                                <p>Hash map will populate as algorithm progresses</p>
                            </div>
                        ) : (
                            <div className="hashmap-entries">
                                <AnimatePresence>
                                    {Object.entries(hashMap).map(([key, value], index) => (
                                        <motion.div
                                            key={key}
                                            className={`hash-entry ${
                                                activeElements.includes('numMap') ? 'just-added' : ''
                                            }`}
                                            initial={{ opacity: 0, x: -30, scale: 0.8 }}
                                            animate={{ opacity: 1, x: 0, scale: 1 }}
                                            exit={{ opacity: 0, x: 30, scale: 0.8 }}
                                            transition={{
                                                duration: 0.5,
                                                delay: index * 0.1,
                                                type: "spring",
                                                stiffness: 300
                                            }}
                                        >
                                            <div className="hash-key-container">
                                                <div className="hash-key">{key}</div>
                                                <div className="key-label">key</div>
                                            </div>

                                            <div className="hash-arrow">
                                                <motion.div
                                                    className="arrow-line"
                                                    initial={{ scaleX: 0 }}
                                                    animate={{ scaleX: 1 }}
                                                    transition={{ duration: 0.3, delay: 0.2 }}
                                                />
                                                <motion.div
                                                    className="arrow-head"
                                                    initial={{ opacity: 0 }}
                                                    animate={{ opacity: 1 }}
                                                    transition={{ duration: 0.2, delay: 0.5 }}
                                                >
                                                    ▶
                                                </motion.div>
                                            </div>

                                            <div className="hash-value-container">
                                                <div className="hash-value">{value}</div>
                                                <div className="value-label">index</div>
                                            </div>
                                        </motion.div>
                                    ))}
                                </AnimatePresence>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Current Operation Display */}
            {(currentOperation.complement !== undefined || currentOperation.target !== undefined) && (
                <motion.div
                    className="operation-display"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4 }}
                >
                    <div className="operation-header">
                        <span className="operation-icon">🔍</span>
                        <h4>Current Operation</h4>
                    </div>

                    <div className="operation-details">
                        {currentOperation.target !== undefined && (
                            <div className="operation-item">
                                <span className="label">Target Sum:</span>
                                <span className="value highlight">{currentOperation.target}</span>
                            </div>
                        )}

                        {currentOperation.currentValue !== undefined && (
                            <div className="operation-item">
                                <span className="label">Current Value:</span>
                                <span className="value">{currentOperation.currentValue}</span>
                                <span className="index-label">(index {currentOperation.currentIndex})</span>
                            </div>
                        )}

                        {currentOperation.complement !== undefined && (
                            <div className="operation-item">
                                <span className="label">Looking for:</span>
                                <span className="value complement">{currentOperation.complement}</span>
                                <span className="formula">
                  ({currentOperation.target} - {currentOperation.currentValue})
                </span>
                            </div>
                        )}
                    </div>
                </motion.div>
            )}

            {/* Algorithm Explanation */}
            <div className="algorithm-explanation">
                <div className="explanation-content">
                    <span className="bulb-icon">💡</span>
                    <p>
                        Hash Map provides <strong>O(1)</strong> lookup time by storing
                        key-value pairs for instant complement checking
                    </p>
                </div>
            </div>
        </div>
    );
};

export default HashMapVisualizer;
