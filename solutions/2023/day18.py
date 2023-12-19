from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 18   01:03:35    3543      0   01:42:12    2150      0
"""

day = 18

def parseInput(lines):
    inst = []
    for l in lines:
        inst.append(l.split())
    return inst


def shoelace(instrs):
    dirs = {
        'R': (0,1),
        'D': (1,0),
        'L': (0,-1),
        'U': (-1,0),
    }
    curr = (0,0)
    coords = []
    for inst in instrs:
        dir = dirs[inst[0]]
        mag = int(inst[1])
        curr = (curr[0] + dir[0] * mag, curr[1] + dir[1] * mag)
        coords.append(curr)

    area = 0
    dist = 0
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        area += (coords[i][0] + coords[j][0]) * (coords[i][1] - coords[j][1])
        dist += manDist(coords[i], coords[j])
    return int(area / 2) + int(dist/2) + 1


def solveA(lines):
    instrs = parseInput(lines)
    return shoelace(instrs)


def solveB(lines):
    instrs = parseInput(lines)
    def decode(inst):
        dist = int(inst[2][2:7], 16)
        dir = "RDLU"[int(inst[2][7])]

        print(dist, dir)
        return (dir, dist)
    return shoelace([decode(i) for i in instrs])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 62, 952408144115)
