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
    if (p1[0] == p2[0]):
        mod = -1 if p1[1] > p2[1] else 1
        return [(p1[0], i) for i in range(p1[1],p2[1]+mod, mod)]
    elif (p1[1] == p2[1]):
        mod = -1 if p1[0] > p2[0] else 1
        return [(i, p1[1]) for i in range(p1[0],p2[0]+mod, mod)]
    elif doDiag:
        # Assume diagonal
        xmod = -1 if p1[0] > p2[0] else 1
        ymod = -1 if p1[1] > p2[1] else 1
        xs = [x for x in range(p1[0],p2[0]+xmod,xmod)]
        ys = [y for y in range(p1[1],p2[1]+ymod,ymod)]
        return [(x,y) for x,y in zip(xs, ys)]
    return []

def solveA(lines):
    theMap = np.zeros((1000,1000), dtype=int)
    for line in lines:
        p1, p2 = parseLine(line)
        for px in pointsBetween(p1, p2):
            theMap[px] += 1
    return len(np.argwhere(theMap >= 2))

def solveB(lines):
    theMap = np.zeros((1000,1000), dtype=int)
    for line in lines:
        p1, p2 = parseLine(line)
        for px in pointsBetween(p1,p2,True):
            theMap[px] += 1
    return len(np.argwhere(theMap >= 2))

answer(solveA, getInput(day), getTestInput(day), 5, True)
answer(solveB, getInput(day), getTestInput(day), 12, True)
