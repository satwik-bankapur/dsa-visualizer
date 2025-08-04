export const detectAlgorithm = (code) => {
    console.log('🔍 Day 14 - Enhanced Algorithm Detection');

    const lowerCode = code.toLowerCase();
    const lines = code.split('\n').map(line => line.trim());

    // Enhanced detection with confidence scores
    const detectionResults = [
        { name: 'Binary Search', score: detectBinarySearch(lowerCode, lines) },
        { name: 'Two Pointers', score: detectTwoPointers(lowerCode, lines) },
        { name: 'Sliding Window', score: detectSlidingWindow(lowerCode, lines) },
        { name: 'Sorting Algorithm', score: detectSorting(lowerCode, lines) },
        { name: 'Dynamic Programming', score: detectDP(lowerCode, lines) },
        { name: 'Tree Traversal', score: detectTreeTraversal(lowerCode, lines) }
    ];

    // Sort by confidence score
    detectionResults.sort((a, b) => b.score - a.score);

    const bestMatch = detectionResults[0];
    console.log('Detection results:', detectionResults);
    console.log('Best match:', bestMatch);

    if (bestMatch.score > 0.3) {
        return bestMatch.name;
    }

    return 'Unknown Algorithm';
};

const detectBinarySearch = (code, lines) => {
    let score = 0;

    // Core patterns (worth more points)
    if (code.includes('left') && code.includes('right')) score += 0.3;
    if (code.includes('mid') || code.includes('middle')) score += 0.4;
    if (code.includes('while') && (code.includes('left') && code.includes('right'))) score += 0.2;
    if (code.includes('//') || code.includes('/') || code.includes('>>')) score += 0.1;

    // Bonus patterns
    if (code.includes('binary') || code.includes('search')) score += 0.2;
    if (code.includes('sorted') || code.includes('ascending')) score += 0.1;

    return Math.min(score, 1.0);
};

const detectTwoPointers = (code, lines) => {
    let score = 0;

    if (code.includes('left') && code.includes('right')) score += 0.3;
    if (code.includes('++') || code.includes('--')) score += 0.2;
    if (code.includes('while') && !code.includes('mid')) score += 0.2;
    if (code.includes('sum') || code.includes('target')) score += 0.2;

    // Penalty if it looks more like binary search
    if (code.includes('mid')) score -= 0.4;

    return Math.max(score, 0);
};

const detectSlidingWindow = (code, lines) => {
    let score = 0;

    if (code.includes('window')) score += 0.4;
    if (code.includes('start') && code.includes('end')) score += 0.3;
    if (code.includes('substring') || code.includes('subarray')) score += 0.2;
    if (code.includes('expand') || code.includes('contract')) score += 0.2;

    return Math.min(score, 1.0);
};

const detectSorting = (code, lines) => {
    let score = 0;

    if (code.includes('sort')) score += 0.4;
    if (code.includes('swap')) score += 0.3;
    if ((code.match(/for/g) || []).length >= 2) score += 0.3;
    if (code.includes('bubble') || code.includes('quick') || code.includes('merge')) score += 0.3;

    return Math.min(score, 1.0);
};

const detectDP = (code, lines) => {
    let score = 0;

    if (code.includes('dp') || code.includes('memo')) score += 0.4;
    if (code.includes('cache') || code.includes('memoization')) score += 0.3;
    if (code.includes('dynamic') || code.includes('programming')) score += 0.2;
    if (code.includes('optimal') || code.includes('subproblem')) score += 0.2;

    return Math.min(score, 1.0);
};

const detectTreeTraversal = (code, lines) => {
    let score = 0;

    if (code.includes('tree') || code.includes('node')) score += 0.3;
    if (code.includes('left') && code.includes('right') && code.includes('root')) score += 0.4;
    if (code.includes('dfs') || code.includes('bfs')) score += 0.3;
    if (code.includes('preorder') || code.includes('inorder') || code.includes('postorder')) score += 0.2;

    return Math.min(score, 1.0);
};
