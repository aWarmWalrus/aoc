from aoc_util import *

import time
import sys
import os
import numpy as np
from collections import deque, defaultdict
from heapq import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 12

def heights(lines, w, h):
    height = np.zeros((len(lines),len(lines[0])), dtype=int)
    for c in range(w):
        for r in range(h):
            ch = lines[r][c]
            if ch == 'S':
                height[r, c] = 0
            elif ch == 'E':
                height[r, c] = 25
            else:
                height[r, c] = ord(lines[r][c]) - 97
    return height


def charToHeight(ch):
    if ch == 'S':
        return 0
    elif ch == 'E':
        return 25
    else:
        return ord(ch) - 97


def chars(lines, w, h):
    chars = np.zeros((len(lines),len(lines[0])), dtype=str)
    for c in range(w):
        for r in range(h):
            chars[r, c] = lines[r][c]
    return chars


def findChar(cMap, char):
    for r in range(cMap.shape[0]):
        for c in range(cMap.shape[1]):
            if cMap[r, c] == char:
                return (r,c)
    return None


def manDist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def aStar(cMap, start, end):
    h, w = cMap.shape

    # gScore
    stepsTo = defaultdict(lambda: 9999999)
    stepsTo[start] = 0

    cameFrom = defaultdict()
    togo = [(manDist(start, end), start)]
    while len(togo) > 0:
        cost, curr = heappop(togo)
        steps = stepsTo[curr]
        if cMap[curr] == "E":
            return steps
        for d in [(-1,0), (0, -1), (1, 0), (0, 1)]:
            newR, newC = (d[0] + curr[0], d[1] + curr[1])
            if newC >= w  or newC < 0 or newR >= h or newR < 0:
                continue
            newPos = (newR, newC)
            if charToHeight(cMap[newPos]) > charToHeight(cMap[curr]) + 1:
                continue

            if steps + 1 < stepsTo[newPos]:
                stepsTo[newPos] = steps + 1
                cameFrom[newPos] = curr
                heappush(togo, (steps + manDist(newPos, end), newPos))
    # No paths lead from start to end
    return 0


def solveA(lines):
    w, h = len(lines[0]), len(lines)
    charMap = chars(lines, w, h)

    start = findChar(charMap, 'S')
    goal = findChar(charMap, 'E')
    print("Using A star to solve this, to go from {} to {}".format(start, goal))
    return aStar(charMap, start, goal)


def solveB(lines):
    w, h = len(lines[0]), len(lines)
    charMap = chars(lines, w, h)
    goal = findChar(charMap, 'E')

    shortestA = 9999
    for c in range(w):
        for r in range(h):
            if charMap[r,c] != "a":
                continue
            pathLen = aStar(charMap, (r,c), goal)
            if pathLen == 0:
                continue
            elif pathLen < shortestA:
                shortestA = pathLen

    return shortestA

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 31, 29)
