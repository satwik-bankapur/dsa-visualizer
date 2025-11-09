class MLAnalysisService {
    constructor() {
        this.baseURL = 'http://localhost:8001';
    }

    async analyzeCode(code, inputData = null) {
        try {
            const requestBody = {
                code_string: code,
                problem_statement: "Algorithm visualization and analysis",
                language: "PYTHON"
            };

            const response = await fetch(`${this.baseURL}/analysis/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Analysis service unavailable`);
            }

            const result = await response.json();
            return this.transformResponse(result);

        } catch (error) {
            throw new Error(`Analysis failed: ${error.message}`);
        }
    }

    transformResponse(mlResponse) {
        const analysis = mlResponse.algorithm_analysis || mlResponse;
        const algorithmType = analysis.primary_pattern || 'UNKNOWN';
        const steps = analysis.execution_steps || [];

        return {
            algorithm: {
                type: algorithmType,
                name: this.formatAlgorithmName(algorithmType),
                confidence: analysis.confidence_score || 0.8
            },
            executionSteps: steps.map((step, index) => ({
                stepNumber: step.step_number || index + 1,
                codeLine: step.code_line || '',
                explanation: step.explanation || 'Processing step...',
                variablesAfter: step.variables_after || {},
                variableChanges: step.variable_changes || {},
                visualizationData: {
                    algorithmType: algorithmType,
                    dataStructures: this.extractDataStructures(step.variables_after || {}),
                    pointers: this.extractPointers(step.variables_after || {}, algorithmType),
                    highlights: []
                }
            })),
            complexity: analysis.complexity_analysis || { time: 'O(n)', space: 'O(1)' },
            metadata: { processingTime: mlResponse.processing_time || 0.1, timestamp: new Date().toISOString() }
        };
    }

    formatAlgorithmName(pattern) {
        const names = {
            'TWO_POINTERS': 'Two Pointers',
            'BINARY_SEARCH': 'Binary Search',
            'HASH_MAP': 'Hash Map'
        };
        return names[pattern] || pattern?.replace(/_/g, ' ') || 'Unknown Algorithm';
    }

    extractDataStructures(variables) {
        const result = {};
        for (let key in variables) {
            if (Array.isArray(variables[key])) {
                result[key] = { type: 'array', values: variables[key] };
            }
        }
        return result;
    }

    extractPointers(variables, algorithmType) {
        const result = {};
        if (algorithmType.includes('Two Pointers') || algorithmType.includes('Binary')) {
            if (variables.left !== undefined) result.left = variables.left;
            if (variables.right !== undefined) result.right = variables.right;
            if (variables.mid !== undefined) result.mid = variables.mid;
        }
        return result;
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}

export default new MLAnalysisService();