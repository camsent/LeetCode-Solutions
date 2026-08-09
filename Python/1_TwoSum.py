from typing import List

# Difficulty = Easy
# Submission Speed ≈ 64.69%

'''
Solution-1: Two-pass Hash Table

Example:
    nums   = [3, 2, 1, 4]
    target = 6

Step 1)
Create a dictionary and populate it with elements of nums as the key
and their corresponding index as values.

    d = {
        3: 0,
        2: 1,
        1: 2,
        4: 3
    }

Step 2)
Traverse the array and for every element, check if the complement
(target - element) exists in the dictionary.

Also check that the index of (target - element) is not the same as
the current index (we use the dictionary values to get indices).

Traversing the array:
    i = 0         nums = [3, 2, 1, 4]
                   ^
    Check if (6 - 3) exists in dictionary:
        Yes, it exists (3 is in d),
        but d[6 - 3] == i
    This means we are using the same element twice, which is invalid.

Step 3)
If we find a valid pair, we return [i, d[complement]].

Time Complexity:  O(N)
Space Complexity: O(N)
'''

# Two-pass
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # First pass: build value -> index mapping
        d = {v: i for i, v in enumerate(nums)}

        # Second pass: check for each element if its complement exists
        for i in range(len(nums)):
            complement = target - nums[i]
            # Ensure complement exists and is not the same index
            if complement in d and d[complement] != i:
                return [i, d[complement]]


'''
Solution-2: Single Pass Hash Table (Optimized)

Instead of doing two passes (one to populate the dictionary and
another to check for complements), we do this in a single pass.

Idea:
    While traversing the array:
        1) For the current element nums[i], compute complement = target - nums[i]
        2) Check if complement is already present in the dictionary:
            - If yes → we have found our answer: [index of complement, i]
        3) If not present → store nums[i] with its index in the dictionary.

This way:
    - We don't need to worry about using the same index twice.
    - We only traverse the list once.

Time Complexity:  O(N)
Space Complexity: O(N)
'''

# Single-pass (this class overrides the previous one in LeetCode-style usage)
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}  # value -> index

        for i in range(len(nums)):
            complement = target - nums[i]

            # If we have already seen the complement, return the pair of indices
            if complement in d:
                return [d[complement], i]

            # Otherwise, store the current value and its index
            d[nums[i]] = i
