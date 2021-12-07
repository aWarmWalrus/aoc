from aoc_util import *
import numpy as np
from functools import partial

"""
[Day 7 Results]
  Part 1
    > time:
    > rank:
  Part 2
    > time:
    > rank:
"""

day = 7

def solve(lines, gasFn):
    crabs = np.array(list(map(int, lines[0].split(','))), dtype=int)
    return min(map(lambda i : sum(map(partial(gasFn, i), crabs)), \
                range(np.amax(crabs))))

def solveA(lines):
    return solve(lines, lambda i, x: abs(x - i))

def solveB(lines):
    def cumulativeDiff(i, x):
        d = abs(x - i)
        return int(d * (d + 1) / 2)
    return solve(lines, cumulativeDiff)

answerAndSubmit(day, solveA, solveB, 37, 168)
