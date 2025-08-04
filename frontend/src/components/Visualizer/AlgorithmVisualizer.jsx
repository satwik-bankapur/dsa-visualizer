import React, { useState, useEffect } from 'react';
import ArrayVisualizer from './ArrayVisualizer';
import PlaybackControls from '../Controls/PlaybackControls';
import './Visualizer.css';

const AlgorithmVisualizer = ({ algorithm, steps, currentStep, onStepChange }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [playInterval, setPlayInterval] = useState(null);
    const [animationSpeed, setAnimationSpeed] = useState(2500); // milliseconds per step

    useEffect(() => {
        return () => {
            if (playInterval) {
                clearInterval(playInterval);
            }
        };
    }, [playInterval]);

    useEffect(() => {
        // Add entrance animation to visualization container
        const container = document.querySelector('.visualization-container');
        if (container && algorithm && steps.length > 0) {
            container.style.animation = 'slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        }
    }, [algorithm, steps]);

    const handlePlay = () => {
        if (currentStep >= steps.length - 1) return;

        setIsPlaying(true);
        const interval = setInterval(() => {
            onStepChange(prevStep => {
                if (prevStep >= steps.length - 1) {
                    setIsPlaying(false);
                    clearInterval(interval);
                    return prevStep;
                }
                return prevStep + 1;
            });
        }, animationSpeed);

        setPlayInterval(interval);
    };

    const handlePause = () => {
        setIsPlaying(false);
        if (playInterval) {
            clearInterval(playInterval);
            setPlayInterval(null);
        }
    };

    const handleNext = () => {
        if (currentStep < steps.length - 1) {
            onStepChange(currentStep + 1);
        }
    };

    const handlePrevious = () => {
        if (currentStep > 0) {
            onStepChange(currentStep - 1);
        }
    };

    const handleReset = () => {
        handlePause();
        onStepChange(0);
    };

    const handleSpeedChange = (newSpeed) => {
        setAnimationSpeed(newSpeed);
        if (isPlaying) {
            handlePause();
            setTimeout(handlePlay, 100); // Restart with new speed
        }
    };

    if (!algorithm || steps.length === 0) {
        return (
            <div className="visualization-container">
                <h2>🎨 Visualization:</h2>
                <div className="welcome-message">
                    <h3>🚀 Day 14 - Interactive Visualizations!</h3>
                    <p>Your React DSA Visualizer is ready for action!</p>
                    <div className="features-list">
                        <h4>✨ New Features Today:</h4>
                        <ul>
                            <li>🎮 Interactive step-by-step controls</li>
                            <li>🎯 Smart speed adjustment</li>
                            <li>📊 Enhanced algorithm detection</li>
                            <li>🎨 Beautiful animations</li>
                        </ul>
                    </div>
                    <div className="supported-algorithms">
                        <h4>Currently Supported:</h4>
                        <ul>
                            <li>🔍 Binary Search</li>
                            <li>👆 Two Pointers</li>
                            <li>🔄 Sorting Algorithms</li>
                            <li>🪟 Sliding Window</li>
                        </ul>
                    </div>
                </div>
            </div>
        );
    }

    const currentStepData = steps[currentStep];

    return (
        <div className="visualization-container">
            <h2>🎨 Interactive Visualization:</h2>

            <div className="viz-header">
                <PlaybackControls
                    currentStep={currentStep}
                    totalSteps={steps.length}
                    isPlaying={isPlaying}
                    onPlay={handlePlay}
                    onPause={handlePause}
                    onNext={handleNext}
                    onPrevious={handlePrevious}
                    onReset={handleReset}
                    animationSpeed={animationSpeed}
                    onSpeedChange={handleSpeedChange}
                />
            </div>

            <ArrayVisualizer
                algorithm={algorithm}
                stepData={currentStepData}
            />

            {/* Progress indicator */}
            <div className="progress-indicator">
                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                    ></div>
                </div>
                <span className="progress-text">
          Progress: {Math.round(((currentStep + 1) / steps.length) * 100)}%
        </span>
            </div>
        </div>
    );
};

export default AlgorithmVisualizer;
