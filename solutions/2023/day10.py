from aoc_util import *

import numpy as np
import regex
from collections import defaultdict
import math

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 10

def parseInput(lines):
    h, w = len(lines), len(lines[0])
    pipes = np.zeros((h,w), dtype=str)
    for (r, c) in np.ndindex(h, w):
        pipes[r, c] = lines[r][c]
    return pipes

def connects(p, coord):
    valid = {
        (-1, 0): "|F7", # Northward, from south
        (1, 0): "|LJ",  # Southward, from north
        (0, -1): "-LF", # Westward, from east
        (0, 1): "-7J",  # Eastward, from west
    }
    neighbors = {
        "|": [(1,0), (-1,0)],
        "-": [(0,1), (0,-1)],
        "7": [(0, -1), (1, 0)],
        "F": [(0, 1), (1, 0)],
        "J": [(0, -1), (-1, 0)],
        "L": [(0, 1), (-1, 0)],
    }
    maxR, maxC = p.shape
    ps = []
    if p[coord] == 'S':
        for d in [(-1,0), (1, 0), (0, -1), (0, 1)]:
            newR, newC = (coord[0]+d[0], coord[1]+d[1])
            if newC >= maxC  or newC < 0 or newR >= maxR or newR < 0:
                continue
            if p[newR, newC] in valid[d]:
                ps.append((newR, newC))
        return ps
    for d in neighbors[p[coord]]:
        newR, newC = (coord[0]+d[0], coord[1]+d[1])
        ps.append((newR, newC))
    return ps


def getPath(pipes, start):
    path = [start]
    prev = start
    curr = connects(pipes, start)[0]
    steps = 0
    while curr != start:
        path.append(curr)
        steps += 1
        next = connects(pipes, curr)
        for n in next:
            if n != prev:
                prev = curr
                curr = n
                break
    return path


def solveA(lines):
    pipes = parseInput(lines)
    (sR, sC) = np.where(pipes == 'S')
    start = (sR[0], sC[0])
    path = getPath(pipes, start)

    pathSet = set(path)
    for r in range(len(lines)):
        acc = ""
        for c in range(len(lines[r])):
            if (r,c) not in pathSet:
                acc += " "
            else:
                acc += lines[r][c]
    return math.floor((len(path) + 1) / 2)


def getSection(pipes, pathSet, coord):
    maxR, maxC = pipes.shape
    queue = [coord]
    section = set()
    isOuter = False
    while len(queue) != 0:
        curr = queue.pop()
        section.add(curr)
        for d in [(-1,0), (1, 0), (0, -1), (0, 1)]:
            newR, newC = (curr[0]+d[0], curr[1]+d[1])
            if newC >= maxC or newC < 0 or newR >= maxR or newR < 0:
                continue
            if (newR, newC) in pathSet:
                continue
            if (newR, newC) in queue:
                continue
            if (newR, newC) in section:
                continue
            queue.append((newR, newC))
            if isOuter:
                continue
            if newR == 0 or newR == maxR - 1 or newC == 0 or newC == maxC - 1:
                isOuter = True
    return section, isOuter


def matchesAt(grid, coord, matcher):
    maxR, maxC = grid.shape
    if coord[0] >= maxR or coord[0] < 0 or coord[1] >= maxC or coord[1] < 0:
        return False
    return grid[coord] in matcher


def enhancify(pipes, pathSet):
    enhanced = np.zeros((pipes.shape[0] * 2, pipes.shape[1] * 2), dtype='str')
    for (r,c) in np.ndindex(enhanced.shape):
        oR = int(r/2)
        oC = int(c/2)
        if (oR, oC) not in pathSet:
            enhanced[r,c] = '.'
        elif r%2 == 0 and c%2 == 0:
            enhanced[r,c] = pipes[oR, oC]
        elif r%2 == 1 and c%2 == 1:
            enhanced[r,c] = '.'
        elif r%2 == 0:    # c%2 == 1 implicitly
            left = (oR, oC)
            right = (oR, oC+1)
            if matchesAt(pipes, left, "-LF") or matchesAt(pipes, right, "-7J"):
                enhanced[r,c] = '-'
            else:
                enhanced[r,c] = '.'
        elif c%2 == 0:    # r%2 == 1 implicitly
            upper = (oR, oC)
            lower = (oR+1, oC)
            if matchesAt(pipes, upper, "|F7") or matchesAt(pipes, lower, "|LJ"):
                enhanced[r,c] = '|'
            else:
                enhanced[r,c] = '.'
    return enhanced


def solveB(lines):
    pipes = parseInput(lines)
    (sR, sC) = np.where(pipes == 'S')
    start = (sR[0], sC[0])

    path = getPath(pipes, start)
    pathSet = set(path)

    enhanced = enhancify(pipes, pathSet)
    (eSR, eSC) = np.where(enhanced == 'S')
    enhancedStart = (eSR[0], eSC[0])
    ePathSet = set(getPath(enhanced, enhancedStart))

    enclosed = 0
    outer = set()
    inner = set()
    for coord in np.ndindex(pipes.shape):
        if coord in pathSet:
            continue
        eCoord = (coord[0] * 2, coord[1] * 2)
        if eCoord in outer:
            continue
        if eCoord in inner:
            enclosed += 1
            continue
        section, isOuter = getSection(enhanced, ePathSet, eCoord)
        if isOuter:
            outer = outer.union(section)
            continue
        else:
            enclosed += 1
            inner = inner.union(section)

    return enclosed


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 80, 10)
