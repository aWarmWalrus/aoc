from aoc_util import *
import numpy as np
from functools import partial

"""
[Day 7 Results]
  Part 1
    > time: 00:07:10
    > rank: 2860
  Part 2
    > time: 00:09:17
    > rank: 1500
"""

day = 7

def solve(lines, gasFn):
    crabs = list(map(int, lines[0].split(',')))
    return min(map(lambda i : sum(map(partial(gasFn, i), crabs)), range(max(crabs))))

def solveA(lines):
    return solve(lines, lambda i, x: abs(x - i))

def solveB(lines):
    def cumulativeDiff(i, x):
        d = abs(x - i)
        return int(d * (d + 1) / 2)
    return solve(lines, cumulativeDiff)

answerAndSubmit(day, solveA, solveB, 37, 168)
