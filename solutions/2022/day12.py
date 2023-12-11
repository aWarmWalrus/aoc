from aoc_util import *
from aoc_algos import *

import numpy as np
from collections import defaultdict
from heapq import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 12

def charToHeight(ch):
    if ch == 'S':
        return 0
    elif ch == 'E':
        return 25
    else:
        return ord(ch) - 97


def solveA(lines):
    charMap = createNumpy2D(lines)
    def canTraverse(src, dst):
        # Wrap up local charMap in closure of this fn.
        return charToHeight(charMap[dst]) - charToHeight(charMap[src]) <= 1

    start = findNumpyValue(charMap, 'S')[0]
    goal = findNumpyValue(charMap, 'E')[0]
    return len(aStar(charMap, start, goal, canTraverse)) - 2


def solveB(lines):
    charMap = createNumpy2D(lines)
    def canTraverse(src, dst):
        # Wrap up local charMap in closure of this fn.
        return charToHeight(charMap[dst]) - charToHeight(charMap[src]) <= 1
    goal = findNumpyValue(charMap, 'E')[0]
    shortestA = 9999
    for (r, c) in np.ndindex(charMap.shape):
        if charMap[r,c] != "a":
            continue
        path = aStar(charMap, (r,c), goal, canTraverse)
        if path == None:
            continue
        elif len(path) < shortestA:
            shortestA = len(path)
    return shortestA - 2

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 31, 29)
