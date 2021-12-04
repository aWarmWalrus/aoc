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
    ups = 0
    for i in range(1, len(lines)):
        if (lines[i] > lines[i-1]):
            ups = ups + 1
    return ups

def solveB(lines):
    windowSize = 3
    ups = 0
    for i in range(windowSize + 1, len(lines)+1):
        j = i - 1
        windowA = sum(lines[j-windowSize:j])
        windowB = sum(lines[i-windowSize:i])
        if (windowB > windowA):
            ups = ups + 1
    return ups

answer(solveA, getInput(day, True), getTestInput(day, True), 7, True)
answer(solveB, getInput(day, True), getTestInput(day, True), 5, True)
