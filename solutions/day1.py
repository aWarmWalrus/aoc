from aoc_util import *

"""
[Day 1 Results]
  Part 1
    > time: 01:03:50
    > rank: 10607
  Part 2
    > time: 01:25:36
    > rank: 10412
"""

day = 1

def solveA(lines):
    nums = list(map(int, lines))
    ups = 0
    for i in range(1, len(nums)):
        if (nums[i] > nums[i-1]):
            ups = ups + 1
    return ups

def solveB(lines):
    nums = list(map(int, lines))
    windowSize = 3
    ups = 0
    for i in range(windowSize + 1, len(nums)+1):
        j = i - 1
        windowA = sum(nums[j-windowSize:j])
        windowB = sum(nums[i-windowSize:i])
        if (windowB > windowA):
            ups = ups + 1
    return ups

answerAndSubmit(day, solveA, solveB, 7, 5)
