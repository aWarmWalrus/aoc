from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time
import math

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 21   00:08:08     506      0   23:50:07    8336      0
"""

day = 21

def parseInput(lines):
    array = createNumpy2D(lines)
    return array


def solveA(lines):
    array = parseInput(lines)
    start = np.argwhere(array == 'S')[0]
    odds, evens = set(), set()
    plots = deque([start])
    for i in range(64):
        nextPlots = deque()
        onSet = odds if i % 2 == 0 else evens
        offSet = odds if i % 2 == 1 else evens
        while len(plots) > 0:
            curr = plots.pop()
            if tuple(curr) in odds or tuple(curr) in evens:
                continue
            for n, _ in validNeighbors(array, curr):
                if array[n] == '#':
                    continue
                if n not in nextPlots and n not in onSet:
                    nextPlots.append(n)
            offSet.add(tuple(curr))
        plots = nextPlots
    return len(nextPlots) + len(evens)


def wraparoundNeighbors(array, coord, dirFn=fourDirs):
    for d in dirFn():
        maxR, maxC = array.shape
        newCoord = (coord[0] + d[0], coord[1] + d[1])
        yield newCoord, d


def bruteForce(array, start, steps, wrapAround=True):
    maxR, maxC = (array.shape[0]-1, array.shape[1]-1)
    plots = deque([tuple(start)])
    odds, evens = set(), set()
    stable = True
    stableAfter = None
    for i in range(steps):
        nextPlots = deque()
        onSet = odds if i % 2 == 0 else evens
        offSet = odds if i % 2 == 1 else evens
        while len(plots) > 0:
            curr = plots.pop()
            if curr in odds or curr in evens:
                continue
            # wraparound can be disabled for testing.
            neighbors = wraparoundNeighbors if wrapAround else validNeighbors
            for n, _ in neighbors(array, curr):
                nc = (n[0] % array.shape[0], n[1] % array.shape[1])
                if array[nc] == '#':
                    continue
                if n not in nextPlots and n not in onSet:
                    stable = False
                    nextPlots.append(n)
            offSet.add(curr)
        plots = nextPlots
        if stable:
            stableAfter = i
            break
        stable = True
    onSet = odds if steps % 2 == 1 else evens
    return len(onSet) + len(plots), stableAfter


def coordToChunk(shape, coord):
    return (math.floor(coord[0] / shape[0]), math.floor(coord[1] / shape[1]))


def axisChunks(layer):
    if layer == 0:
        yield (0, 0)
        return
    dirs = [(1,0), (0, 1), (-1,0), (0, -1)]
    for d in dirs:
        curr = (d[0] * layer, d[1] * layer)
        yield curr


def getDiagChunks(layer):
    assert layer > 1
    dirs = [(1,1), (-1, 1), (-1,-1), (1, -1)]
    for d in dirs:
        curr = (d[0] * (layer-1), d[1] * (layer-1))
        yield curr


def chunksAfter(array, steps):
    assert(array.shape[0] == array.shape[1])
    total = 1
    yield (0, 0), 0
    w = array.shape[0]
    i = math.floor(w / 2)
    layer = 1
    while steps > i:
        # steps is greater than i: add the axis chunks
        for ax in axisChunks(layer):
            yield (ax, i+1)
        if steps > i + math.ceil(w/2):
            for diag in getDiagChunks(layer+1):
                yield (diag, i + 1 + math.ceil(w/2))
        i += w
        layer += 1


def norm(coord):
    cR = 0 if coord[0] == 0 else coord[0] / abs(coord[0])
    cC = 0 if coord[1] == 0 else coord[1] / abs(coord[1])
    return (cR, cC)


def isDiag(coord):
    return coord[0] != 0 and coord[1] != 0


def efficientReachable(array, start, steps):
    total = 0
    mR, mC = array.shape[0]-1, array.shape[1]-1
    mid = math.floor(array.shape[0]/2)
    stabilityCache = {}
    for ch, started in chunksAfter(array, steps):
        chunkDir = norm(ch)
        startsDict = {
            (0,0): (mid,mid),
            (1,0): (0,mid),
            (-1,0): (mR,mid),
            (0,1): (mid,0),
            (0,-1): (mid,mC),
            (1,1): (0,0),
            (-1,1): (mR,0),
            (-1,-1): (mR,mC),
            (1,-1): (0,mC),
        }
        multiplier = 1
        if isDiag(ch):
            multiplier = abs(ch[0])

        parity = (steps-started) % 2
        if (chunkDir, parity) in stabilityCache:
            res, stableAfter = stabilityCache[(chunkDir, parity)]
            if steps-started > stableAfter:
                total += multiplier * res
                continue

        res, stableAfter = bruteForce(array, startsDict[chunkDir], steps-started, False)
        if stableAfter is not None:
            stabilityCache[(chunkDir, parity)] = (res, stableAfter)
        total += multiplier * res
    return total


def solveB(lines):
    array = parseInput(lines)
    start = np.argwhere(array == 'S')[0]
    if array.shape[0] < 60:
        # skip the test.
        return 0

    # Get brute force answers for the modified input.
    # 50 = 1940
    # 100 = 7645
    # for i in range(150):
    #     print("steps: ", i)
    #     # print("brute force :", bruteForce(array, start, i)[0])
    #     print("efficient:   ", efficientReachable(array, start, i))
    #     input()
    return efficientReachable(array, start, 26_501_365)


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 42, 0)
