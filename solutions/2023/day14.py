from aoc_util import *
from aoc_algos import *

import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 14

def parseInput(lines):
    plat = createNumpy2D(lines)
    return plat


def tiltPlatform(platform, rocks, dir="N"):
    plat=platform

    score = 0
    sRocks = sorted(rocks, key=lambda x: x[0])
    if dir == 'S':
        sRocks = sorted(rocks, key=lambda x: x[0], reverse=True)
    elif dir == 'E':
        sRocks = sorted(rocks, key=lambda x: x[1], reverse=True)
    elif dir == 'W':
        sRocks = sorted(rocks, key=lambda x: x[1])

    for i in range(len(sRocks)):
        (r,c) = sRocks[i]
        score += plat.shape[0] - r
        if dir == "N":
            if r == 0:
                sRocks[i] = (r,c)
                continue
            if plat[r-1,c] == '.':
                moved = True
                target = r-1
                plat[r,c] = '.'
                while target > 0 and plat[target-1,c] == '.':
                    target -= 1
                plat[target,c] = 'O'
                sRocks[i] = (target,c)
        elif dir == "S":
            if r == plat.shape[0]-1:
                sRocks[i] = (r,c)
                continue
            if plat[r+1,c] == '.':
                moved = True
                plat[r,c] = '.'
                target = r+1
                while target < plat.shape[0]-1 and plat[target+1,c] == '.':
                    target += 1
                plat[target,c] = 'O'
                sRocks[i] = (target,c)
        elif dir == "E":
            if c == plat.shape[1]-1:
                sRocks[i] = (r,c)
                continue
            if plat[r,c+1] == '.':
                moved = True
                plat[r,c] = '.'
                target = c+1
                while target < plat.shape[1]-1 and plat[r,target+1] == '.':
                    target += 1
                plat[r,target] = 'O'
                sRocks[i] = (r,target)
        elif dir == "W":
            if c == 0:
                sRocks[i] = (r,c)
                continue
            if plat[r,c-1] == '.':
                moved = True
                plat[r,c] = '.'
                target = c-1
                while target > 0 and plat[r,target-1] == '.':
                    target -= 1
                plat[r,target] = 'O'
                sRocks[i] = (r,target)
    score = 0
    for i in range(len(sRocks)):
        score += plat.shape[0] - sRocks[i][0]

    return plat, sRocks, score


def printPlat(plat):
    print()
    for r in range(plat.shape[0]):
        print("".join(plat[r]))


def solveA(lines):
    plat = parseInput(lines)
    rocks = []
    for r in np.argwhere(plat == 'O'):
        rocks.append(tuple(r))
    return tiltPlatform(plat, rocks)[2]


def findCycle(plat):
    rocks = []
    for r in np.argwhere(plat == 'O'):
        rocks.append(tuple(r))
    cycles = 1
    i = 0
    printPlat(plat)
    check = time.time()
    lookup = {}
    lookup[plat.data.tobytes()] = (cycles, plat)
    hashCache = set()
    scores = []
    while cycles < 1_000_000_000:
        plat, rocks, _ = tiltPlatform(plat, rocks, "N")
        plat, rocks, _ = tiltPlatform(plat, rocks, "W")
        plat, rocks, _ = tiltPlatform(plat, rocks, "S")
        plat, rocks, score = tiltPlatform(plat, rocks, "E")
        scores.append(score)
        if plat.data.tobytes() in lookup.keys():
            print(cycles, plat, lookup[plat.data.tobytes()])
            input()
            return cycles, lookup[plat.data.tobytes()][0], scores
        else:
            lookup[plat.data.tobytes()] = (cycles, plat)
        if cycles % 10_000 == 0:
            now = time.time()
            print("\nCycle {}    elapsed time: {}s".format(cycles, now-check))
            check = now
            printPlat(plat)
        cycles += 1
    print("this ain't ever happening chief")


def solveB(lines):
    plat = parseInput(lines)
    end, start, scores = findCycle(plat)
    print(end, start, scores)
    cycle = end-start

    return scores[start + ((1_000_000_000 - start - 1) % cycle)]


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 136, 64)
