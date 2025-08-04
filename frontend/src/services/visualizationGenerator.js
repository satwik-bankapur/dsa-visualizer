export const generateVisualizationSteps = (algorithm, parsedData) => {
    const steps = [];

    if (algorithm === 'Binary Search') {
        return generateBinarySearchSteps(parsedData);
    } else if (algorithm === 'Two Pointers') {
        return generateTwoPointersSteps(parsedData);
    }

    return [{
        type: 'simple',
        description: `${algorithm} visualization coming soon!`,
        data: parsedData
    }];
};

const generateBinarySearchSteps = (parsedData) => {
    const array = parsedData.arrays.length > 0 ? parsedData.arrays[0] : [1, 3, 5, 7, 9, 11];
    const target = parsedData.target || 7;

    const steps = [];
    let left = 0;
    let right = array.length - 1;

    steps.push({
        type: 'binary_search',
        description: `Starting Binary Search for target ${target}`,
        array: [...array],
        target,
        left,
        right,
        mid: null,
        found: false,
        explanation: `Initialize: left = ${left}, right = ${right}. Array: [${array.join(', ')}]`
    });

    let stepCount = 1;
    while (left <= right && stepCount < 10) {
        const mid = Math.floor((left + right) / 2);

        steps.push({
            type: 'binary_search',
            description: `Step ${stepCount}: Calculate mid = ${mid}`,
            array: [...array],
            target,
            left,
            right,
            mid,
            found: false,
            explanation: `Mid index is ${mid}, value is ${array[mid]}. Comparing ${array[mid]} with target ${target}.`
        });

        if (array[mid] === target) {
            steps.push({
                type: 'binary_search',
                description: `Found target ${target} at index ${mid}!`,
                array: [...array],
                target,
                left,
                right,
                mid,
                found: true,
                explanation: `Success! Target ${target} found at index ${mid}. Search complete!`
            });
            break;
        } else if (array[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
        stepCount++;
    }

    return steps;
};

const generateTwoPointersSteps = (parsedData) => {
    return [{
        type: 'two_pointers',
        description: 'Two Pointers algorithm detected',
        data: parsedData,
        explanation: 'Two Pointers visualization will be implemented soon!'
    }];
};
