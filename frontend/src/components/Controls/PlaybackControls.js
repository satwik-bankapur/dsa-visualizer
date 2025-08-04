import React from 'react';

const PlaybackControls = ({
                              currentStep,
                              totalSteps,
                              isPlaying,
                              onPlay,
                              onPause,
                              onNext,
                              onPrevious,
                              onReset,
                              animationSpeed,
                              onSpeedChange
                          }) => {
    const speedOptions = [
        { label: '0.5x', value: 5000 },
        { label: '1x', value: 2500 },
        { label: '1.5x', value: 1500 },
        { label: '2x', value: 1000 }
    ];

    return (
        <div className="playback-controls">
            <button
                onClick={onPrevious}
                disabled={currentStep === 0}
                className="control-btn prev-btn"
                title="Previous Step"
            >
                ⏮️ Prev
            </button>

            <button
                onClick={isPlaying ? onPause : onPlay}
                disabled={currentStep >= totalSteps - 1}
                className="control-btn play-pause-btn"
                title={isPlaying ? "Pause Animation" : "Play Animation"}
            >
                {isPlaying ? '⏸️ Pause' : '▶️ Play'}
            </button>

            <button
                onClick={onNext}
                disabled={currentStep >= totalSteps - 1}
                className="control-btn next-btn"
                title="Next Step"
            >
                Next ⏭️
            </button>

            <button
                onClick={onReset}
                className="control-btn reset-btn"
                title="Reset to Beginning"
            >
                🔄 Reset
            </button>

            {/* Speed Control */}
            <div className="speed-control">
                <label htmlFor="speed-select">Speed:</label>
                <select
                    id="speed-select"
                    value={animationSpeed}
                    onChange={(e) => onSpeedChange(parseInt(e.target.value))}
                    className="speed-selector"
                >
                    {speedOptions.map(option => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>
            </div>

            <span className="step-info">
        Step {currentStep + 1} of {totalSteps}
      </span>
        </div>
    );
};

export default PlaybackControls;
