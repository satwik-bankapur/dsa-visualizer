// components/Controls/PlaybackControls.jsx
import React from 'react';
import './PlaybackControls.css';

const PlaybackControls = ({
                              isPlaying,
                              currentStep,
                              totalSteps,
                              speed,
                              onPlay,
                              onPause,
                              onStep,
                              onReset,
                              onSpeedChange
                          }) => {
    if (totalSteps === 0) {
        return (
            <div className="playback-controls">
                <div className="no-steps">
                    <p>🎬 Playback controls will appear here after code analysis</p>
                </div>
            </div>
        );
    }

    const progressPercent = totalSteps > 0 ? (currentStep / (totalSteps - 1)) * 100 : 0;

    return (
        <div className="playback-controls">
            <div className="controls-header">
                <h3>Step Navigation</h3>
                <div className="step-counter">
                    <span className="current">{currentStep + 1}</span>
                    <span className="separator">/</span>
                    <span className="total">{totalSteps}</span>
                </div>
            </div>

            <div className="progress-section">
                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${progressPercent}%` }}
                    />
                    <div
                        className="progress-thumb"
                        style={{ left: `${progressPercent}%` }}
                    />
                </div>
            </div>

            <div className="control-buttons">
                <button
                    className="control-btn reset"
                    onClick={onReset}
                    disabled={currentStep === 0}
                    title="Reset to beginning"
                >
                    ⏮️
                </button>

                <button
                    className="control-btn prev"
                    onClick={() => onStep(-1)}
                    disabled={currentStep === 0}
                    title="Previous step"
                >
                    ⏪
                </button>

                <button
                    className={`control-btn play-pause ${isPlaying ? 'playing' : ''}`}
                    onClick={isPlaying ? onPause : onPlay}
                    title={isPlaying ? 'Pause' : 'Play'}
                >
                    {isPlaying ? '⏸️' : '▶️'}
                </button>

                <button
                    className="control-btn next"
                    onClick={() => onStep(1)}
                    disabled={currentStep >= totalSteps - 1}
                    title="Next step"
                >
                    ⏩
                </button>

                <button
                    className="control-btn end"
                    onClick={() => onStep(totalSteps - 1 - currentStep)}
                    disabled={currentStep >= totalSteps - 1}
                    title="Jump to end"
                >
                    ⏭️
                </button>
            </div>

            <div className="speed-control">
                <label htmlFor="speed-slider">Speed:</label>
                <div className="speed-slider-container">
                    <span className="speed-label">Fast</span>
                    <input
                        id="speed-slider"
                        type="range"
                        min="100"
                        max="3000"
                        step="100"
                        value={speed}
                        onChange={(e) => onSpeedChange(Number(e.target.value))}
                        className="speed-slider"
                    />
                    <span className="speed-label">Slow</span>
                </div>
                <span className="speed-value">{speed}ms</span>
            </div>
        </div>
    );
};

export default PlaybackControls;
