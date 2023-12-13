from aoc_util import *
from aoc_algos import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 13   00:40:23    3143      0   01:09:04    3173      0
"""

day = 13

def parseInput(lines):
    mirrors = []
    last = 0
    for i in range(len(lines)):
        if len(lines[i]) == 0:
            mirrors.append(createNumpy2D(lines[last:i], dtype=int, transformFn=lambda x: 1 if x=='#' else 0))
            last = i+1
    mirrors.append(createNumpy2D(lines[last:], dtype=int, transformFn=lambda x: 1 if x=='#' else 0))
    return mirrors


def reflect(m, oldScore = 0):
    for r in range(1, m.shape[0]):
        if 100 * r == oldScore:
            continue
        flipped = np.flip(m[r:], 0)
        trunc = abs(flipped.shape[0] - r)

        if flipped.shape[0] < r:
            top = m[trunc : r]
            bottom = flipped
        elif flipped.shape[0] >= r:
            top = m[:r]
            bottom = flipped[trunc:]

        if np.array_equal(top, bottom):
            return 100 * r

    for c in range(1, m.shape[1]):
        if c == oldScore:
            continue
        flipped = np.flip(m[:, c:], 1)
        trunc = abs(flipped.shape[1] - c)

        if flipped.shape[1] < c:
            left = m[:, trunc:c]
            right = flipped
        elif flipped.shape[1] >= c:
            left = m[:, :c]
            right = flipped[:, trunc:]

        if np.array_equal(left, right):
            return c
    return 0


def findSmudge(m):
    oldScore = reflect(m)
    for (r,c) in np.ndindex(m.shape):
        m[r,c] ^= 1
        pts = reflect(m, oldScore)
        m[r,c] ^= 1
        if pts != 0:
            return pts
    exit("error!")


def solveA(lines):
    mirrors = parseInput(lines)
    return sum([reflect(m) for m in mirrors])


def solveB(lines):
    mirrors = parseInput(lines)
    return sum([findSmudge(m) for m in mirrors])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 405, 400)
