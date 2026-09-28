#Speed = 95.26%
#Memory = 21.54%
#Time Complexity: O(n)
#Space Complexity: O(1)

#I had to add "from typing import list" at the top to get it to work


class Solution: 
    def maxSubArray(self, nums: List[int]) -> int:
        maxSub = nums[0]
        curSum = 0

        for n in nums:
            if curSum < 0:
                curSum = 0
            curSum += n
            maxSub = max(maxSub, curSum)
        return maxSub

