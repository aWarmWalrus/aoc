import numpy as np
import bisect
import heapq
import time
from aoc_util import *
from collections import defaultdict
from collections import deque

"""
[Day 15 Results]
  Part 1
    > time: 00:29:45
    > rank: 1976
  Part 2
    > time: 00:53:47
    > rank: 1682
"""

day = 15

def parseLines(lines):
    grid = np.zeros((len(lines), len(lines[0])))
    for i in range(len(lines)):
        grid[i] = np.array([int(j) for j in lines[i]])
    return grid


def getNeighbors(c, grid):
    ns = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    for nx,ny in ns:
        newC = (c[0]+nx, c[1]+ny)
        if grid[newC] < np.inf:
            neighbors.append(newC)
    return neighbors


"""
Maintain a sorted list, using bisection to quickly insert a new node into the
list while maintaining the list sort.

This is apparently pretty much as good as using a heap.
"""
def dijsktra(g):
    grid = np.pad(g, 1, 'constant', constant_values=np.inf)
    risks = defaultdict(lambda : np.inf)
    unvisited = [(0, (1,1))]
    while unvisited:
        currRisk, curr = unvisited.pop(0)
        for n in getNeighbors(curr, grid):
            v = currRisk + grid[n]
            if v < risks[n]:
                bisect.insort(unvisited, (v,n))
                risks[n] = v
    return risks[g.shape]


"""
Use a heap to maintain the priority queue.
"""
def dijsktraHeap(g):
    grid = np.pad(g, 1, 'constant', constant_values=np.inf)
    risks = defaultdict(lambda : np.inf)
    unvisited = [(0, (1,1))]
    heapq.heapify(unvisited)
    while len(unvisited) > 0:
        currRisk, curr = heapq.heappop(unvisited)
        for n in getNeighbors(curr, grid):
            v = currRisk + grid[n]
            if v < risks[n]:
                heapq.heappush(unvisited, (v, n))
                risks[n] = v
    return risks[g.shape]


def solveA(lines, optimal=False):
    return int(dijsktra(parseLines(lines)))


def solveB(lines, optimize=True):
    grid = parseLines(lines)
    gX, gY = grid.shape
    newGrid = np.zeros((gX * 5, gY * 5))
    for i in range(5):
        for j in range(5):
            newSection = (grid + i + j - 1) % 9 + 1
            newGrid[gX * i : gX * (i + 1), gY * j : gY * (j + 1)] = newSection
    if optimize:
        return int(dijsktraHeap(newGrid))
    else:
        return int(dijsktra(newGrid))

answerAndSubmit(day, solveA, solveB, 40, 315)

debug("\n > Performance testing...")
tic = time.time()
solveB(getInput(day), optimize=False)
toc = time.time()
debug("Dijsktra with sorted list: {}ms".format(int((toc-tic) * 1000)))

tic = time.time()
solveB(getInput(day), optimize=True)
toc = time.time()
debug("Dijsktra with priority queue: {}ms".format(int((toc-tic) * 1000)))
