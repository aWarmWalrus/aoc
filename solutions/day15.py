import numpy as np
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
    grid = np.zeros((len(lines), len(lines[0])), dtype=int)
    for i in range(len(lines)):
        grid[i] = np.array([int(j) for j in lines[i]])
    return grid

def getNeighbors(coord, m):
    ns = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = deque()
    for ne in ns:
        nx = coord[0] + ne[0]
        ny = coord[1] + ne[1]
        if m[nx,ny] < 999:
            neighbors.appendleft((nx,ny))
    return neighbors

def dijsktra(g):
    grid = np.pad(g, 1, 'constant', constant_values=99999)
    curr = (1,1)
    riskMap = defaultdict(lambda : 99999)
    riskMap[curr] = 0
    unvisited = deque([curr])
    while len(unvisited) > 0:
        curr = unvisited.pop()
        neighbors = getNeighbors(curr, grid)
        for n in neighbors:
            if grid[n] == 99999:
                continue
            v = riskMap[curr] + grid[n]
            if v < riskMap[n]:
                unvisited.appendleft(n)
                riskMap[n] = v
    return riskMap[g.shape]

def solveA(lines, optimal=False):
    oGrid = parseLines(lines)
    return dijsktra(parseLines(lines))

def generateFullGrid(grid):
    gX, gY = grid.shape
    newGrid = np.zeros((gX * 5, gY * 5), dtype=int)
    for i in range(5):
        for j in range(5):
            newSection = (grid + i + j - 1) % 9 + 1
            newGrid[gX * i : gX * (i + 1), gY * j : gY * (j + 1)] = newSection
    return newGrid

def solveB(lines):
    oGrid = generateFullGrid(parseLines(lines))
    return dijsktra(oGrid)

answerAndSubmit(day, solveA, solveB, 40, 315)
