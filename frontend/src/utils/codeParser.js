export const parseCodeInput = (code, customArray, customTarget) => {
    const parseResult = {
        arrays: [],
        target: null,
        variables: {},
        functions: []
    };

    try {
        // Use custom data if provided
        if (customArray) {
            const numbers = customArray.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
            if (numbers.length > 0) {
                parseResult.arrays.push(numbers);
            }
        }

        if (customTarget) {
            parseResult.target = parseInt(customTarget);
        }

        // Parse arrays from code if no custom data
        if (parseResult.arrays.length === 0) {
            parseResult.arrays = extractArrays(code);
        }

        // Parse target values
        if (!parseResult.target) {
            parseResult.target = extractTarget(code);
        }

    } catch (error) {
        console.log('Parsing error:', error);
        // Fallback values
        parseResult.arrays = [[1, 3, 5, 7, 9, 11, 13, 15, 17, 19]];
        parseResult.target = 7;
    }

    return parseResult;
};

const extractArrays = (code) => {
    const arrays = [];
    const arrayPatterns = [
        /\[([^\[\]]*)\]/g,
        /arr\s*=\s*\[([^\[\]]*)\]/g,
        /array\s*=\s*\[([^\[\]]*)\]/g,
        /nums\s*=\s*\[([^\[\]]*)\]/g,
    ];

    arrayPatterns.forEach(pattern => {
        let match;
        while ((match = pattern.exec(code)) !== null) {
            const arrayContent = match[1].trim();
            if (arrayContent) {
                const numbers = parseNumberArray(arrayContent);
                if (numbers.length > 0) {
                    arrays.push(numbers);
                }
            }
        }
    });

    if (arrays.length === 0) {
        arrays.push([1, 3, 5, 7, 9, 11, 13, 15, 17, 19]);
    }

    return arrays;
};

const parseNumberArray = (content) => {
    try {
        return content.split(',')
            .map(item => item.trim())
            .filter(item => item !== '')
            .map(item => {
                const num = parseFloat(item);
                return isNaN(num) ? item : num;
            })
            .filter(item => typeof item === 'number');
    } catch (error) {
        return [];
    }
};

const extractTarget = (code) => {
    const targetPatterns = [
        /target\s*=\s*(\d+)/i,
        /find\s*\(\s*(\d+)\s*\)/i,
        /search\s*\(\s*.*?,\s*(\d+)\s*\)/i,
        /== (\d+)/,
        /target:\s*(\d+)/i
    ];

    for (const pattern of targetPatterns) {
        const match = code.match(pattern);
        if (match) {
            return parseInt(match[1]);
        }
    }

    return 7; // Default target
};
