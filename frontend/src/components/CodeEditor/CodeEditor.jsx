// components/CodeEditor/CodeEditor.jsx
import React, { useRef, useEffect } from 'react';
import './CodeEditor.css';

const CodeEditor = ({ value, onChange, placeholder, readOnly = false }) => {
    const textareaRef = useRef(null);

    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            // Auto-resize functionality
            const adjustHeight = () => {
                textarea.style.height = 'auto';
                textarea.style.height = Math.max(200, textarea.scrollHeight) + 'px';
            };

            adjustHeight();
            textarea.addEventListener('input', adjustHeight);

            return () => textarea.removeEventListener('input', adjustHeight);
        }
    }, [value]);

    const handleKeyDown = (e) => {
        // Tab key functionality
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = e.target.selectionStart;
            const end = e.target.selectionEnd;
            const newValue = value.substring(0, start) + '    ' + value.substring(end);
            onChange(newValue);

            // Move cursor after the inserted spaces
            setTimeout(() => {
                e.target.selectionStart = e.target.selectionEnd = start + 4;
            }, 0);
        }

        // Ctrl+A to select all
        if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
            e.preventDefault();
            e.target.select();
        }
    };

    return (
        <div className="code-editor">
            <div className="editor-header">
                <div className="editor-tabs">
                    <div className="tab active">
                        <span className="tab-icon">🐍</span>
                        <span>algorithm.py</span>
                    </div>
                </div>
                <div className="editor-actions">
                    <button className="action-btn" title="Clear Code">
                        🗑️
                    </button>
                    <button className="action-btn" title="Copy Code">
                        📋
                    </button>
                </div>
            </div>

            <div className="editor-content">
                <div className="line-numbers">
                    {value.split('\n').map((_, index) => (
                        <div key={index + 1} className="line-number">
                            {index + 1}
                        </div>
                    ))}
                </div>

                <textarea
                    ref={textareaRef}
                    className="code-textarea"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={placeholder}
                    readOnly={readOnly}
                    spellCheck="false"
                    autoComplete="off"
                    autoCorrect="off"
                    autoCapitalize="off"
                />
            </div>

            <div className="editor-footer">
                <span className="language-indicator">Python</span>
                <span className="cursor-position">
          Ln {(value.substring(0, value.indexOf('\n')) || value).length}, Col 1
        </span>
            </div>
        </div>
    );
};

export default CodeEditor;
