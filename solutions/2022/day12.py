from aoc_util import *

import time
import sys
import os
import numpy as np
from collections import deque
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
                height[r, c] = 26
            else:
                height[r, c] = ord(lines[r][c]) - 97
    return height


def manDist(a, b):
    return abs(a[0] - b[0]) + 2 * abs(a[1] - b[1])

def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def solveA(lines):
    w, h = len(lines[0]), len(lines)
    hMap = heights(lines, w, h)

    def findChar(lines, char):
        for r in range(len(lines)):
            for c in range(len(lines[r])):
                if lines[r][c] == char:
                    return (r,c)
        return None

    goal = findChar(lines, 'E')
    start = findChar(lines, 'S')
    print(hMap)

    def aStar():
        visited = set({start})
        cameFrom = defaultdict(0)
        costs = defaultdict(9999999)
        costs[start] = 0
        togo = [(dist(start, goal), 0, start)]
        dirs = [(-1,0), (0, -1), (1, 0), (0, 1)]
        while len(togo) > 0:
            cost, steps, curr = heappop(togo)
            if hMap[curr] == 26:
                return steps
            for d in dirs:
                newR, newC = (d[0] + curr[0], d[1] + curr[1])
                if newC >= w  or newC < 0 or newR >= h or newR < 0:
                    continue
                newPos = (newR, newC)
                if newPos in visited:
                    continue
                if hMap[newPos] > hMap[curr] + 1:
                    continue
                visited.add(newPos)
                costEst = costs[curr]
                heappush(togo, (steps + dist(newPos, goal), steps + 1, newPos))
        return 0

    print("Using A star to solve this, to go from {} to {}".format(start, goal))
    return aStar()

def solveB(lines):
    return 0

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 31, 1)
