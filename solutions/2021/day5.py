from aoc_util import *
import numpy as np

"""
[Day 5 Results]
  Part 1
    > time: 00:14:04
    > rank: 1373
  Part 2
    > time: 00:33:18
    > rank: 2389
"""

day = 5

def parseLine(line):
    point1, point2 = line.split(" -> ")
    x1, y1 = point1.split(',')
    x2, y2 = point2.split(',')
    return (int(x1), int(y1)), (int(x2), int(y2))

def pointsBetween(p1, p2, doDiag = False):
    def offByOne(v1,v2):
        return -1 if v1 > v2 else 1

    if (p1[0] == p2[0]):
        m = offByOne(p1[1], p2[1])
        return [(p1[0], i) for i in range(p1[1],p2[1]+m, m)]
    elif (p1[1] == p2[1]):
        m = offByOne(p1[0], p2[0])
        return [(i, p1[1]) for i in range(p1[0],p2[0]+m, m)]
    elif doDiag:
        # Assume diagonal
        xm = offByOne(p1[0], p2[0])
        xs = range(p1[0], p2[0] + xm, xm)
        ym = offByOne(p1[1], p2[1])
        ys = range(p1[1], p2[1] + ym, ym)
        return zip(xs, ys)
    return []

def solve(lines, doDiags):
    theMap = np.zeros((1000,1000), dtype=int)
    for line in lines:
        p1, p2 = parseLine(line)
        for px in pointsBetween(p1, p2, doDiags):
            theMap[px] += 1
    return np.count_nonzero(theMap >= 2)

def solveA(lines):
    return solve(lines, False)

def solveB(lines):
    return solve(lines, True)

answerAndSubmit(day, solveA, solveB, 5, 12)
