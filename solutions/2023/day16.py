from aoc_util import *
from aoc_algos import *

from collections import deque
import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 16   00:22:04     835      0   00:27:02     712      0
"""

day = 16

def parseInput(lines):
    map = createNumpy2D(lines)
    return map


def shineBeam(curr, dir, map):
    beams = [(curr, dir)]
    energized = set()
    seen = set()
    while len(beams) > 0:
        curr, dir = beams.pop()
        if (curr, dir) in seen or isOob(map, curr):
            continue
        energized.add(curr)
        seen.add((curr, dir))
        if map[curr] == '.' or \
                (map[curr] == '|' and dir[1] == 0) or \
                (map[curr] == '-' and dir[0] == 0):
            next = (curr[0] + dir[0], curr[1] + dir[1])
            beams.append((next, dir))
        elif (map[curr] == '-' and dir[1] == 0):
            nL = (curr[0], curr[1] - 1)
            nR = (curr[0], curr[1] + 1)
            beams.append((nL, (0, -1)))
            beams.append((nR, (0, 1)))
        elif (map[curr] == '|' and dir[0] == 0):
            nU = (curr[0] - 1, curr[1])
            nD = (curr[0] + 1, curr[1])
            beams.append((nU, (-1, 0)))
            beams.append((nD, (1, 0)))
        elif map[curr] == '\\':
            nextDir = (dir[1], dir[0])
            next = (curr[0] + nextDir[0], curr[1] + nextDir[1])
            beams.append((next, nextDir))
        elif map[curr] == '/':
            nextDir = (-dir[1], -dir[0])
            next = (curr[0] + nextDir[0], curr[1] + nextDir[1])
            beams.append((next, nextDir))
    return len(energized)


def solveA(lines):
    inp = parseInput(lines)
    return shineBeam((0,0), (0,1), inp)


def solveB(lines):
    inp = parseInput(lines)
    best = 0
    maxR = inp.shape[0]-1
    maxC = inp.shape[1]-1
    for r in range(inp.shape[0]):
        enR = shineBeam((r,0), (0,1), inp)
        enL = shineBeam((r,maxC), (0,-1), inp)
        if max(enR, enL) > best:
            best = max(enR, enL)
    for c in range(inp.shape[1]):
        enD = shineBeam((0,c), (1,0), inp)
        enU = shineBeam((maxR,c), (-1,0), inp)
        if max(enD, enU) > best:
            best = max(enD, enU)
    return best


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 46, 51)
