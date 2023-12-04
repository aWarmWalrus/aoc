from aoc_util import *

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


def getCharMap(lines):
    h, w = len(lines), len(lines[0])
    chars = np.zeros((h,w), dtype=str)
    for (r, c) in np.ndindex(h, w):
        chars[r, c] = lines[r][c]
    return chars


def findChar(charMap, char):
    for (r, c) in np.ndindex(charMap.shape):
        if charMap[r, c] == char:
            return (r, c)
    return None



def aStar(charMap, start, end):
    # Use manhattan distance since can't travel diagonally.
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # gScore is the cost of the cheapest known path from start to each node.
    stepsTo = defaultdict(lambda: 99999)
    stepsTo[start] = 0

    cameFrom = defaultdict()
    togo = [(distance(start, end), start)]
    while len(togo) > 0:
        cost, curr = heappop(togo)
        steps = stepsTo[curr]
        # Reached the goal
        if charMap[curr] == "E":
            return steps

        for d in [(-1,0), (0, -1), (1, 0), (0, 1)]:
            maxR, maxC = charMap.shape
            newR, newC = (curr[0] + d[0], curr[1] + d[1])
            if newC >= maxC  or newC < 0 or newR >= maxR or newR < 0:
                continue

            newPos = (newR, newC)
            if charToHeight(charMap[newPos]) > charToHeight(charMap[curr]) + 1:
                continue

            if steps + 1 < stepsTo[newPos]:
                stepsTo[newPos] = steps + 1
                cameFrom[newPos] = curr
                # fScore is our best guess as to how cheap a path could be from
                # start to finish if it goes through this node.
                fScore = steps + distance(newPos, end)
                heappush(togo, (fScore, newPos))
                
    # No paths lead from start to end
    return 0


def solveA(lines):
    charMap = getCharMap(lines)
    start = findChar(charMap, 'S')
    goal = findChar(charMap, 'E')
    return aStar(charMap, start, goal)


def solveB(lines):
    charMap = getCharMap(lines)
    goal = findChar(charMap, 'E')
    shortestA = 9999
    for (r, c) in np.ndindex(charMap.shape):
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
