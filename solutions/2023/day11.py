from aoc_util import *
from aoc_algos import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 11   00:19:48    2047      0   00:32:57    2490      0
"""

day = 11

def parseInput(lines):
    return createNumpy2D(lines, dtype=int, transformFn= lambda v: 1 if v == '#' else 0)

    
def expanded(gals, coord, expandBy):
    newR = coord[0]
    for r in range(coord[0]):
        if sum(gals[r]) == 0:
            newR += expandBy
    newC = coord[1]
    for c in range(coord[1]):
        if sum(gals[:, c]) == 0:
            newC += expandBy
    return (newR, newC)


def solveA(lines):
    map = parseInput(lines)
    gals = np.argwhere(map == 1)
    eGals = [expanded(map, g, 1) for g in gals]
    sum = 0
    for g1 in range(len(eGals)):
        for g2 in range(g1 + 1, len(eGals)):
            sum += manDist(eGals[g1], eGals[g2])
    return sum


def solveB(lines):
    map = parseInput(lines)
    gals = np.argwhere(map == 1)
    eGals = [expanded(map, g, 999999) for g in gals]
    sum = 0
    for g1 in range(len(eGals)):
        for g2 in range(g1 + 1, len(eGals)):
            sum += manDist(eGals[g1], eGals[g2])
    return sum


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 374, 82000210)
