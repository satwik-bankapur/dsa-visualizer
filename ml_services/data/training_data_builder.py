# ml_services/data/training_data_builder.py
import ast
from typing import List, Tuple
from models.internal_models import AlgorithmPattern

class TrainingDataBuilder:
    """Build training data for algorithm pattern recognition"""

    def __init__(self):
        self.training_samples = []

    def add_samples(self) -> List[Tuple[ast.AST, str, AlgorithmPattern]]:
        """Add manually curated training samples"""

        # Hash Map samples (expanded)
        hash_map_samples = [
            # Two Sum
            ("""
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
""", AlgorithmPattern.HASH_MAP),

            # Contains Duplicate
            ("""
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
""", AlgorithmPattern.HASH_MAP),

            # Group Anagrams
            ("""
def group_anagrams(strs):
    anagram_map = {}
    for s in strs:
        key = ''.join(sorted(s))
        if key not in anagram_map:
            anagram_map[key] = []
        anagram_map[key].append(s)
    return list(anagram_map.values())
""", AlgorithmPattern.HASH_MAP),

            # Valid Anagram
            ("""
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    for char in t:
        if char not in count:
            return False
        count[char] -= 1
        if count[char] == 0:
            del count[char]
    
    return len(count) == 0
""", AlgorithmPattern.HASH_MAP),

            # First Unique Character
            ("""
def first_unique_char(s):
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    return -1
""", AlgorithmPattern.HASH_MAP),

            # Intersection of Two Arrays
            ("""
def intersection(nums1, nums2):
    set1 = set(nums1)
    result = set()
    
    for num in nums2:
        if num in set1:
            result.add(num)
    
    return list(result)
""", AlgorithmPattern.HASH_MAP),

            # Jewels and Stones
            ("""
def num_jewels_in_stones(jewels, stones):
    jewel_set = set(jewels)
    count = 0
    
    for stone in stones:
        if stone in jewel_set:
            count += 1
    
    return count
""", AlgorithmPattern.HASH_MAP),

            # Top K Frequent Elements
            ("""
def top_k_frequent(nums, k):
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    
    return sorted(count.keys(), key=lambda x: count[x], reverse=True)[:k]
""", AlgorithmPattern.HASH_MAP),

            # Subarray Sum Equals K
            ("""
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for num in nums:
        prefix_sum += num
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
""", AlgorithmPattern.HASH_MAP),

            # Word Pattern
            ("""
def word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    
    char_to_word = {}
    word_to_char = {}
    
    for char, word in zip(pattern, words):
        if char in char_to_word:
            if char_to_word[char] != word:
                return False
        else:
            char_to_word[char] = word
        
        if word in word_to_char:
            if word_to_char[word] != char:
                return False
        else:
            word_to_char[word] = char
    
    return True
""", AlgorithmPattern.HASH_MAP),
        ]

        # Two Pointers samples (expanded)
        two_pointers_samples = [
            # Valid Palindrome
            ("""
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
""", AlgorithmPattern.TWO_POINTERS),

            # Two Sum II
            ("""
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return []
""", AlgorithmPattern.TWO_POINTERS),

            # Container With Most Water
            ("""
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
""", AlgorithmPattern.TWO_POINTERS),

            # 3Sum
            ("""
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    
    return result
""", AlgorithmPattern.TWO_POINTERS),

            # Remove Duplicates from Sorted Array
            ("""
def remove_duplicates(nums):
    if not nums:
        return 0
    
    write_ptr = 1
    for read_ptr in range(1, len(nums)):
        if nums[read_ptr] != nums[read_ptr - 1]:
            nums[write_ptr] = nums[read_ptr]
            write_ptr += 1
    
    return write_ptr
""", AlgorithmPattern.TWO_POINTERS),

            # Move Zeros
            ("""
def move_zeros(nums):
    write_ptr = 0
    
    for read_ptr in range(len(nums)):
        if nums[read_ptr] != 0:
            nums[write_ptr] = nums[read_ptr]
            write_ptr += 1
    
    while write_ptr < len(nums):
        nums[write_ptr] = 0
        write_ptr += 1
""", AlgorithmPattern.TWO_POINTERS),

            # Reverse String
            ("""
def reverse_string(s):
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
""", AlgorithmPattern.TWO_POINTERS),

            # Trapping Rain Water
            ("""
def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
""", AlgorithmPattern.TWO_POINTERS),

            # Sort Colors
            ("""
def sort_colors(nums):
    left, curr, right = 0, 0, len(nums) - 1
    
    while curr <= right:
        if nums[curr] == 0:
            nums[left], nums[curr] = nums[curr], nums[left]
            left += 1
            curr += 1
        elif nums[curr] == 2:
            nums[curr], nums[right] = nums[right], nums[curr]
            right -= 1
        else:
            curr += 1
""", AlgorithmPattern.TWO_POINTERS),

            # Palindromic Substrings
            ("""
def count_substrings(s):
    count = 0
    
    for i in range(len(s)):
        # Odd length palindromes
        left, right = i, i
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
        
        # Even length palindromes
        left, right = i, i + 1
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    return count
""", AlgorithmPattern.TWO_POINTERS),
        ]

        # Sliding Window samples (expanded)
        sliding_window_samples = [
            # Longest Substring Without Repeating Characters
            ("""
def length_of_longest_substring(s):
    left = 0
    max_len = 0
    char_set = set()
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len
""", AlgorithmPattern.SLIDING_WINDOW),

            # Maximum Subarray Sum of Size K
            ("""
def max_subarray_sum(nums, k):
    left = 0
    max_sum = float('-inf')
    window_sum = 0
    
    for right in range(len(nums)):
        window_sum += nums[right]
        
        if right - left + 1 == k:
            max_sum = max(max_sum, window_sum)
            window_sum -= nums[left]
            left += 1
    
    return max_sum
""", AlgorithmPattern.SLIDING_WINDOW),

            # Minimum Window Substring
            ("""
def min_window(s, t):
    if not s or not t:
        return ""
    
    dict_t = {}
    for char in t:
        dict_t[char] = dict_t.get(char, 0) + 1
    
    required = len(dict_t)
    left, right = 0, 0
    formed = 0
    window_counts = {}
    
    ans = float("inf"), None, None
    
    while right < len(s):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
        
        while left <= right and formed == required:
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            char = s[left]
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            
            left += 1
        
        right += 1
    
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]
""", AlgorithmPattern.SLIDING_WINDOW),

            # Longest Repeating Character Replacement
            ("""
def character_replacement(s, k):
    left = 0
    max_len = 0
    max_count = 0
    count = {}
    
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_count = max(max_count, count[s[right]])
        
        if right - left + 1 - max_count > k:
            count[s[left]] -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
""", AlgorithmPattern.SLIDING_WINDOW),

            # Permutation in String
            ("""
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    s1_count = {}
    for char in s1:
        s1_count[char] = s1_count.get(char, 0) + 1
    
    window_count = {}
    left = 0
    
    for right in range(len(s2)):
        window_count[s2[right]] = window_count.get(s2[right], 0) + 1
        
        if right - left + 1 == len(s1):
            if window_count == s1_count:
                return True
            window_count[s2[left]] -= 1
            if window_count[s2[left]] == 0:
                del window_count[s2[left]]
            left += 1
    
    return False
""", AlgorithmPattern.SLIDING_WINDOW),

            # Find All Anagrams in a String
            ("""
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    
    p_count = {}
    for char in p:
        p_count[char] = p_count.get(char, 0) + 1
    
    window_count = {}
    result = []
    left = 0
    
    for right in range(len(s)):
        window_count[s[right]] = window_count.get(s[right], 0) + 1
        
        if right - left + 1 == len(p):
            if window_count == p_count:
                result.append(left)
            window_count[s[left]] -= 1
            if window_count[s[left]] == 0:
                del window_count[s[left]]
            left += 1
    
    return result
""", AlgorithmPattern.SLIDING_WINDOW),

            # Maximum Average Subarray I
            ("""
def find_max_average(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum / k
""", AlgorithmPattern.SLIDING_WINDOW),

            # Fruits into Baskets
            ("""
def total_fruit(fruits):
    left = 0
    max_len = 0
    basket = {}
    
    for right in range(len(fruits)):
        basket[fruits[right]] = basket.get(fruits[right], 0) + 1
        
        while len(basket) > 2:
            basket[fruits[left]] -= 1
            if basket[fruits[left]] == 0:
                del basket[fruits[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
""", AlgorithmPattern.SLIDING_WINDOW),
        ]

        # Binary Search samples (expanded)
        binary_search_samples = [
            # Standard Binary Search
            ("""
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
""", AlgorithmPattern.BINARY_SEARCH),

            # Find First Bad Version
            ("""
def first_bad_version(n):
    left, right = 1, n
    
    while left < right:
        mid = (left + right) // 2
        if is_bad_version(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
""", AlgorithmPattern.BINARY_SEARCH),

            # Search Insert Position
            ("""
def search_insert(nums, target):
    left, right = 0, len(nums)
    
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
""", AlgorithmPattern.BINARY_SEARCH),

            # Find Peak Element
            ("""
def find_peak_element(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left
""", AlgorithmPattern.BINARY_SEARCH),

            # Search in Rotated Sorted Array
            ("""
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
""", AlgorithmPattern.BINARY_SEARCH),

            # Find Minimum in Rotated Sorted Array
            ("""
def find_min(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    
    return nums[left]
""", AlgorithmPattern.BINARY_SEARCH),

            # Search a 2D Matrix
            ("""
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // n][mid % n]
        
        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False
""", AlgorithmPattern.BINARY_SEARCH),

            # Koko Eating Bananas
            ("""
def min_eating_speed(piles, h):
    left, right = 1, max(piles)
    
    def can_finish(k):
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k
        return hours <= h
    
    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
""", AlgorithmPattern.BINARY_SEARCH),

            # Time Based Key-Value Store
            ("""
def get(key, timestamp):
    if key not in self.data:
        return ""
    
    values = self.data[key]
    left, right = 0, len(values) - 1
    result = ""
    
    while left <= right:
        mid = (left + right) // 2
        if values[mid][1] <= timestamp:
            result = values[mid][0]
            left = mid + 1
        else:
            right = mid - 1
    
    return result
""", AlgorithmPattern.BINARY_SEARCH),
        ]

        # DFS samples (expanded)
        dfs_samples = [
            # Binary Tree Inorder Traversal
            ("""
def inorder_traversal(root):
    result = []
    
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    
    dfs(root)
    return result
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Number of Islands
            ("""
def num_islands(grid):
    if not grid:
        return 0
    
    count = 0
    
    def dfs(i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        dfs(i+1, j)
        dfs(i-1, j)
        dfs(i, j+1)
        dfs(i, j-1)
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    
    return count
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Maximum Depth of Binary Tree
            ("""
def max_depth(root):
    if not root:
        return 0
    
    def dfs(node):
        if not node:
            return 0
        left_depth = dfs(node.left)
        right_depth = dfs(node.right)
        return max(left_depth, right_depth) + 1
    
    return dfs(root)
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Path Sum
            ("""
def has_path_sum(root, target_sum):
    def dfs(node, current_sum):
        if not node:
            return False
        
        current_sum += node.val
        
        if not node.left and not node.right:
            return current_sum == target_sum
        
        return dfs(node.left, current_sum) or dfs(node.right, current_sum)
    
    return dfs(root, 0)
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Validate Binary Search Tree
            ("""
def is_valid_bst(root):
    def dfs(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (dfs(node.left, min_val, node.val) and 
                dfs(node.right, node.val, max_val))
    
    return dfs(root, float('-inf'), float('inf'))
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Balanced Binary Tree
            ("""
def is_balanced(root):
    def dfs(node):
        if not node:
            return 0, True
        
        left_height, left_balanced = dfs(node.left)
        right_height, right_balanced = dfs(node.right)
        
        balanced = (left_balanced and right_balanced and 
                   abs(left_height - right_height) <= 1)
        height = max(left_height, right_height) + 1
        
        return height, balanced
    
    return dfs(root)[1]
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Binary Tree Right Side View
            ("""
def right_side_view(root):
    result = []
    
    def dfs(node, level):
        if not node:
            return
        
        if level == len(result):
            result.append(node.val)
        
        dfs(node.right, level + 1)
        dfs(node.left, level + 1)
    
    dfs(root, 0)
    return result
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Course Schedule
            ("""
def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses
    
    def dfs(node):
        if color[node] == GRAY:
            return False
        if color[node] == BLACK:
            return True
        
        color[node] = GRAY
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        color[node] = BLACK
        return True
    
    for i in range(num_courses):
        if not dfs(i):
            return False
    return True
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),

            # Word Search
            ("""
def exist(board, word):
    def dfs(i, j, index):
        if index == len(word):
            return True
        if (i < 0 or i >= len(board) or j < 0 or j >= len(board[0]) or 
            board[i][j] != word[index]):
            return False
        
        temp = board[i][j]
        board[i][j] = '#'
        
        found = (dfs(i+1, j, index+1) or dfs(i-1, j, index+1) or
                dfs(i, j+1, index+1) or dfs(i, j-1, index+1))
        
        board[i][j] = temp
        return found
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if dfs(i, j, 0):
                return True
    return False
""", AlgorithmPattern.DEPTH_FIRST_SEARCH),
        ]

        # Dynamic Programming samples (expanded)
        dp_samples = [
            # Fibonacci
            ("""
def fibonacci(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Climbing Stairs
            ("""
def climb_stairs(n):
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # House Robber
            ("""
def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[-1]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Coin Change
            ("""
def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != amount + 1 else -1
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Longest Increasing Subsequence
            ("""
def length_of_lis(nums):
    if not nums:
        return 0
    
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # 0/1 Knapsack
            ("""
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], 
                              dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Longest Common Subsequence
            ("""
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Maximum Subarray
            ("""
def max_subarray(nums):
    max_so_far = max_ending_here = nums[0]
    
    for i in range(1, len(nums)):
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Word Break
            ("""
def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[len(s)]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),

            # Unique Paths
            ("""
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]
""", AlgorithmPattern.DYNAMIC_PROGRAMMING),
        ]

        # Greedy samples (expanded)
        greedy_samples = [
            # Jump Game
            ("""
def can_jump(nums):
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True
""", AlgorithmPattern.GREEDY),

            # Activity Selection
            ("""
def activity_selection(activities):
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return selected
""", AlgorithmPattern.GREEDY),

            # Gas Station
            ("""
def can_complete_circuit(gas, cost):
    total_tank = current_tank = start = 0
    
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]
        
        if current_tank < 0:
            start = i + 1
            current_tank = 0
    
    return start if total_tank >= 0 else -1
""", AlgorithmPattern.GREEDY),

            # Best Time to Buy and Sell Stock
            ("""
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    
    return max_profit
""", AlgorithmPattern.GREEDY),

            # Meeting Rooms II
            ("""
def min_meeting_rooms(intervals):
    start_times = sorted([i[0] for i in intervals])
    end_times = sorted([i[1] for i in intervals])
    
    start_ptr = end_ptr = 0
    used_rooms = 0
    
    while start_ptr < len(intervals):
        if start_times[start_ptr] >= end_times[end_ptr]:
            used_rooms -= 1
            end_ptr += 1
        
        used_rooms += 1
        start_ptr += 1
    
    return used_rooms
""", AlgorithmPattern.GREEDY),

            # Non-overlapping Intervals
            ("""
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 0
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]
    
    return count
""", AlgorithmPattern.GREEDY),

            # Queue Reconstruction by Height
            ("""
def reconstruct_queue(people):
    people.sort(key=lambda x: (-x[0], x[1]))
    result = []
    
    for person in people:
        result.insert(person[1], person)
    
    return result
""", AlgorithmPattern.GREEDY),

            # Minimum Number of Arrows
            ("""
def find_min_arrows(points):
    if not points:
        return 0
    
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    
    for start, balloon_end in points[1:]:
        if start > end:
            arrows += 1
            end = balloon_end
    
    return arrows
""", AlgorithmPattern.GREEDY),

            # Task Scheduler
            ("""
def least_interval(tasks, n):
    task_counts = {}
    for task in tasks:
        task_counts[task] = task_counts.get(task, 0) + 1
    
    max_count = max(task_counts.values())
    max_count_tasks = sum(1 for count in task_counts.values() if count == max_count)
    
    return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)
""", AlgorithmPattern.GREEDY),

            # Candy
            ("""
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    
    # Left to right pass
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    
    # Right to left pass
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    
    return sum(candies)
""", AlgorithmPattern.GREEDY),
        ]

        # BFS samples
        bfs_samples = [
            # Binary Tree Level Order Traversal
            ("""
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
""", AlgorithmPattern.BREADTH_FIRST_SEARCH),

            # Shortest Path in Binary Matrix
            ("""
from collections import deque

def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    while queue:
        row, col, path_len = queue.popleft()
        
        if row == n-1 and col == n-1:
            return path_len
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < n and 0 <= new_col < n and 
                grid[new_row][new_col] == 0 and (new_row, new_col) not in visited):
                queue.append((new_row, new_col, path_len + 1))
                visited.add((new_row, new_col))
    
    return -1
""", AlgorithmPattern.BREADTH_FIRST_SEARCH),

            # Word Ladder
            ("""
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    if end_word not in word_list:
        return 0
    
    word_set = set(word_list)
    queue = deque([(begin_word, 1)])
    visited = set([begin_word])
    
    while queue:
        word, length = queue.popleft()
        
        if word == end_word:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                
                if new_word in word_set and new_word not in visited:
                    queue.append((new_word, length + 1))
                    visited.add(new_word)
    
    return 0
""", AlgorithmPattern.BREADTH_FIRST_SEARCH),

            # Rotting Oranges
            ("""
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh_count += 1
    
    if fresh_count == 0:
        return 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    time = 0
    
    while queue:
        row, col, curr_time = queue.popleft()
        time = curr_time
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                grid[new_row][new_col] == 1):
                grid[new_row][new_col] = 2
                fresh_count -= 1
                queue.append((new_row, new_col, curr_time + 1))
    
    return time if fresh_count == 0 else -1
""", AlgorithmPattern.BREADTH_FIRST_SEARCH),
        ]

        # Combine all samples
        all_samples = (hash_map_samples + two_pointers_samples +
                       sliding_window_samples + binary_search_samples +
                       dfs_samples + dp_samples + greedy_samples + bfs_samples)

        # Parse code strings to AST
        training_data = []
        for code_str, pattern in all_samples:
            try:
                tree = ast.parse(code_str.strip())
                training_data.append((tree, code_str.strip(), pattern))
            except SyntaxError as e:
                print(f"Syntax error in sample: {e}")
                continue

        return training_data
