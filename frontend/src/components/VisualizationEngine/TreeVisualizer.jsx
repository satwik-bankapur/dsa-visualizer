// components/VisualizationEngine/TreeVisualizer.jsx
import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './TreeVisualizer.css';

const TreeVisualizer = ({
                            data,
                            highlights = [],
                            pointers = {},
                            algorithmType
                        }) => {
    // For now, we'll create a simple tree structure for demonstration
    // This can be enhanced based on your ml_services tree data format
    const treeData = useMemo(() => {
        // Example binary tree structure - adapt based on your data format
        if (data.tree) return data.tree;

        // Default example tree for demonstration
        return {
            value: 10,
            left: {
                value: 5,
                left: { value: 3, left: null, right: null },
                right: { value: 7, left: null, right: null }
            },
            right: {
                value: 15,
                left: { value: 12, left: null, right: null },
                right: { value: 18, left: null, right: null }
            }
        };
    }, [data]);

    const renderNode = (node, level = 0, position = 'root', parentId = '') => {
        if (!node) return null;

        const nodeId = `${parentId}-${position}-${level}`;
        const isHighlighted = highlights.includes(node.value);
        const isCurrentPointer = pointers.current === node.value;
        const isVisited = pointers.visited?.includes(node.value);

        return (
            <motion.div
                key={nodeId}
                className={`tree-node-container level-${level}`}
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: level * 0.1 }}
            >
                <div className="node-content">
                    <motion.div
                        className={`tree-node ${isHighlighted ? 'highlighted' : ''} ${
                            isCurrentPointer ? 'current' : ''
                        } ${isVisited ? 'visited' : ''}`}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <span className="node-value">{node.value}</span>
                        {isCurrentPointer && (
                            <motion.div
                                className="current-indicator"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 0.3 }}
                            >
                                👈
                            </motion.div>
                        )}
                    </motion.div>

                    {(node.left || node.right) && (
                        <div className="children-container">
                            <div className="children">
                                <div className="child-branch left-branch">
                                    {node.left && <div className="connection-line" />}
                                    {renderNode(node.left, level + 1, 'left', nodeId)}
                                </div>
                                <div className="child-branch right-branch">
                                    {node.right && <div className="connection-line" />}
                                    {renderNode(node.right, level + 1, 'right', nodeId)}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </motion.div>
        );
    };

    return (
        <div className="tree-visualizer">
            <div className="tree-header">
                <div className="tree-info">
                    <span className="tree-icon">🌳</span>
                    <h4>Binary Tree Structure</h4>
                </div>
                <div className="traversal-type">
          <span className="algorithm-badge">
            {algorithmType?.replace(/_/g, ' ') || 'Tree Traversal'}
          </span>
                </div>
            </div>

            <div className="tree-container">
                <AnimatePresence>
                    {treeData ? (
                        renderNode(treeData)
                    ) : (
                        <div className="no-tree">
                            <div className="no-tree-icon">🌱</div>
                            <p>Tree structure will be displayed here</p>
                        </div>
                    )}
                </AnimatePresence>
            </div>

            {/* Traversal Information */}
            {pointers.traversalOrder && (
                <motion.div
                    className="traversal-info"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h4>Traversal Order:</h4>
                    <div className="traversal-sequence">
                        {pointers.traversalOrder.map((value, index) => (
                            <motion.span
                                key={index}
                                className="traversal-item"
                                initial={{ opacity: 0, scale: 0.5 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                {value}
                            </motion.span>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Algorithm Explanation */}
            <div className="algorithm-explanation">
                <div className="explanation-content">
                    <span className="info-icon">ℹ️</span>
                    <div className="explanation-text">
                        {algorithmType === 'DEPTH_FIRST_SEARCH' && (
                            <p>
                                <strong>Depth-First Search (DFS):</strong> Explores as far down each branch
                                as possible before backtracking. Uses a stack (or recursion).
                            </p>
                        )}
                        {algorithmType === 'BREADTH_FIRST_SEARCH' && (
                            <p>
                                <strong>Breadth-First Search (BFS):</strong> Explores all nodes at the current
                                level before moving to the next level. Uses a queue.
                            </p>
                        )}
                        {!algorithmType?.includes('SEARCH') && (
                            <p>
                                <strong>Tree Traversal:</strong> Systematic way of visiting all nodes
                                in a tree data structure exactly once.
                            </p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TreeVisualizer;
