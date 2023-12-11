from aoc_util import *
from aoc_algos import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  8   00:26:47    4787      0   00:41:06    3802      0
"""

day = 8

def solveA(lines):
    trees = createNumpy2D(lines, dtype=int)
    visible = np.zeros(trees.shape, dtype=int)
    h = trees.shape[0]
    w = trees.shape[1]
    for (r, c) in np.ndindex(trees.shape):
        if r == 0 or r == h-1 or c == 0 or c == w - 1:
            visible[r,c] = 1
            continue
        sightlines = [trees[r, :c], trees[r, c+1:], trees[:r, c], trees[r+1:, c]]
        if any([trees[r,c] > max(s) for s in sightlines]):
            visible[r,c] = 1
    return np.sum(visible)


def solveB(lines):
    trees = createNumpy2D(lines, dtype=int)
    visible = np.zeros(trees.shape, dtype=int)

    def viewScore(r, c):
        dirs = [trees[r, c+1:], reversed(trees[r, :c]), trees[r+1:, c], reversed(trees[:r, c])]
        ans = 1
        base = trees[r,c]
        for sightlines in dirs:
            num = 0
            for tree in sightlines:
                num += 1
                if tree >= base:
                    break
            ans *= num
        return ans

    return max([viewScore(r,c) for (r,c) in np.ndindex(trees.shape)])

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 21, 8)
