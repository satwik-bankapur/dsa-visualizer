const codeInput = document.getElementById('codeInput');
const visualizeBtn = document.getElementById('visualizeBtn');
const visualization = document.getElementById('visualization');

function detectAlgorithm(code) {
    // Convert to lowercase for easier detection
    const lowerCode = code.toLowerCase();

    // Check for binary search
    if (lowerCode.includes('left') && lowerCode.includes('right') && lowerCode.includes('mid')) {
        return 'Binary Search';
    }

    // Check for two pointers
    if (lowerCode.includes('left') && lowerCode.includes('right') && lowerCode.includes('while')) {
        return 'Two Pointers';
    }

    // Check for sorting
    if (lowerCode.includes('sort') || (lowerCode.includes('for') && lowerCode.includes('swap'))) {
        return 'Sorting Algorithm';
    }

    return 'Unknown Algorithm';
}
function visualizeBinarySearch() {
    const steps = [
        "Initialize: left = 0, right = array.length - 1",
        "Calculate mid = (left + right) / 2",
        "Compare arr[mid] with target",
        "If match found, return mid",
        "If arr[mid] < target, search right half (left = mid + 1)",
        "If arr[mid] > target, search left half (right = mid - 1)",
        "Repeat until found or left > right"
    ];

    let stepsHTML = '<h3>🔍 Binary Search Steps:</h3>';
    steps.forEach((step, index) => {
        stepsHTML += `<div class="step">Step ${index + 1}: ${step}</div>`;
    });

    // Sample array visualization
    stepsHTML += `
        <h4>Example with array [1, 3, 5, 7, 9, 11] searching for 7:</h4>
        <div class="array-visualization">
            <div class="array-element left-pointer">1</div>
            <div class="array-element">3</div>
            <div class="array-element mid-pointer">5</div>
            <div class="array-element">7</div>
            <div class="array-element">9</div>
            <div class="array-element right-pointer">11</div>
        </div>
        <p>Yellow = Left pointer, Orange = Right pointer, Green = Mid pointer</p>
    `;

    return stepsHTML;
}

function visualizeTwoPointers() {
    return `
        <h3>👆 Two Pointers Technique:</h3>
        <div class="step">Step 1: Place one pointer at start, one at end</div>
        <div class="step">Step 2: Move pointers based on condition</div>
        <div class="step">Step 3: Continue until pointers meet</div>
        <div class="array-visualization">
            <div class="array-element left-pointer">👈 Left</div>
            <div class="array-element">...</div>
            <div class="array-element">...</div>
            <div class="array-element right-pointer">Right 👉</div>
        </div>
    `;
}

function visualizeSorting() {
    return `
        <h3>🔄 Sorting Algorithm:</h3>
        <div class="step">Step 1: Compare adjacent elements</div>
        <div class="step">Step 2: Swap if needed</div>
        <div class="step">Step 3: Repeat until sorted</div>
        <div class="array-visualization">
            <div class="array-element">3</div>
            <div class="array-element mid-pointer">1</div>
            <div class="array-element mid-pointer">4</div>
            <div class="array-element">2</div>
        </div>
        <p>Green elements are being compared/swapped</p>
    `;
}

// Update your main click handler:
visualizeBtn.addEventListener('click', function() {
    const userCode = codeInput.value;

    if (userCode.trim() === '') {
        visualization.innerHTML = '<p style="color: red;">Please paste some code first!</p>';
        return;
    }

    const algorithm = detectAlgorithm(userCode);

    let output = `<h3>🎯 Detected Algorithm: ${algorithm}</h3>`;

    if (algorithm === 'Binary Search') {
        output += visualizeBinarySearch();
    } else if (algorithm === 'Two Pointers') {
        output += visualizeTwoPointers();
    } else if (algorithm === 'Sorting Algorithm') {
        output += visualizeSorting();
    } else {
        output += '<p>Visualization for this algorithm is not available yet.</p>';
    }

    output += `
        <div style="margin-top: 20px;">
            <h4>Your Code:</h4>
            <pre style="background: #eee; padding: 10px; border-radius: 5px; overflow-x: auto;">${userCode}</pre>
        </div>
    `;

    visualization.innerHTML = output;
});