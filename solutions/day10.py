from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter
from functools import partial

"""
[Day 9 Results]
  Part 1
    > time: 00:14:38
    > rank: 3126
  Part 2
    > time: 00:42:11
    > rank: 3202
"""

day = 9

def parseMap(lines):
    heatmap = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i in range(len(lines)):
        heatmap[i] = np.array([int(v) for v in lines[i]])
    return heatmap

def neighbors(point, max, filterFn = None):
    nlist = []
    for n in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx = point[0] + n[0]
        ny = point[1] + n[1]
        if (nx >= 0 and nx < max[0] and ny >= 0 and ny < max[1]):
            if filterFn is None or filterFn((nx,ny)):
                nlist.append((nx,ny))
    return nlist

def isLowest(adjValues, value):
    lowest = True
    for a in adjValues:
        if value >= a:
            lowest = False
    return lowest

def getLows(heatmap):
    lows = []
    for row in range(heatmap.shape[0]):
        for col in range(heatmap.shape[1]):
            ns = [heatmap[n] for n in neighbors((row, col), heatmap.shape)]
            if isLowest(ns, heatmap[row,col]):
                lows.append((row,col))
    return lows

def solveA(lines):
    heatmap = parseMap(lines)
    return sum([heatmap[low] + 1 for low in getLows(heatmap)])

def solveB(lines):
    heatmap = parseMap(lines)
    basinSizes = []
    for coord in getLows(heatmap):
        # do bfs until you see a 9 or out of bounds.
        goto = [coord]
        visited = []
        while len(goto) > 0:
            next = goto.pop()
            visited.append(next)
            filter = lambda p: heatmap[p] < 9 and p not in visited + goto
            adj = neighbors(next, heatmap.shape, filterFn=filter)
            goto += adj
        basinSizes.append(len(visited))

    largest = sorted(basinSizes, reverse=True)[0:3]
    mul = 1
    for i in largest:
        mul *= i
    return mul

answerAndSubmit(day, solveA, solveB, 15, 1134)
