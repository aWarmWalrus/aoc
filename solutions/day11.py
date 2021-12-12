from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter
from functools import partial
from statistics import median

"""
[Day 11 Results]
  Part 1
    > time:
    > rank:
  Part 2
    > time:
    > rank:
"""

day = 11

def parseLines(lines):
    octos = np.zeros((10,10))
    for i in range(len(lines)):
        octos[i] = np.array([int(i) for i in lines[i]])
    return np.pad(octos, 1, constant_values=-np.inf)

def incrementNeighbors(p, octos):
    for d in [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]:
        nx = p[0] + d[0]
        ny = p[1] + d[1]
        octos[nx,ny] += 1
    return octos

KERNEL = [[1, 1, 1],
          [1, 0, 1],
          [1, 1, 1]]

def solveA(lines):
    octos = parseLines(lines)
    totalFlashes = 0
    for s in range(100):
        # Step 1: increment all octopii by one.
        octos += 1

        # Step 2: every octopus > 9 flashes, and increments its neighbors.
        flashed = np.zeros_like(octos).astype(bool)
        while (toFlash := ((octos > 9) & ~flashed)).any():
            for nx, ny in np.argwhere(toFlash):
                octos[nx-1:nx+2, ny-1:ny+2] += KERNEL
            flashed |= toFlash

        # Step 3: every octopus that flashed gets set to 0.
        octos[flashed] = 0
        totalFlashes += flashed.sum()
    return totalFlashes

def solveB(lines):
    octos = parseLines(lines)

    totalFlashes = 0
    steps = 1000
    for s in range(1000):
        # Step 1: increment all octopii by one.
        octos += 1

        # Step 2: every octopus > 9 flashes, and increments its neighbors.
        flashed = np.zeros_like(octos).astype(bool)
        while (toFlash := ((octos > 9) & ~flashed)).any():
            for nx, ny in np.argwhere(toFlash):
                octos[nx-1:nx+2, ny-1:ny+2] += KERNEL
            flashed |= toFlash

        # Step 3: every octopus that flashed gets set to 0.
        octos[flashed] = 0
        if flashed[1:-1, 1:-1].all():
            return s + 1
        totalFlashes += flashed.sum()

    return 0

answerAndSubmit(day, solveA, solveB, 1656, 195)
