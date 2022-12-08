from aoc_util import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  8   00:26:47    4787      0   00:41:06    3802      0
"""

day = 8

def getTrees(lines, w, h):
    trees = np.zeros((len(lines),len(lines[0])), dtype=int)
    for c in range(w):
        for r in range(h):
            trees[c, r] = int(lines[c][r])
    return trees


def solveA(lines):
    h = len(lines)
    w = len(lines[0])
    visible = np.zeros((h,w), dtype=int)
    trees = getTrees(lines, w, h)
    for c in range(w):
        for r in range(h):
            if r == 0 or r == h-1 or c == 0 or c == w - 1:
                visible[c, r] = 1
                continue
            sightlines = [trees[:c, r], trees[c+1:, r], trees[c, :r], trees[c, r+1:]]
            if any([trees[c, r] > max(s) for s in sightlines]):
                visible[c, r] = 1
    return np.sum(visible)


def solveB(lines):
    h = len(lines)
    w = len(lines[0])
    visible = np.zeros((len(lines),len(lines[0])), dtype=int)
    trees = getTrees(lines, w, h)

    def numViewedTrees(trees, c, r):
        dirs = [trees[c+1:, r], reversed(trees[:c, r]), trees[c, r+1:], reversed(trees[c, :r])]
        ans = 1
        base = trees[c][r]
        for sightlines in dirs:
            num = 0
            for tree in sightlines:
                num += 1
                if tree >= base:
                    break
            ans *= num
        return ans

    return max([max([numViewedTrees(trees, c, r) for c in range(w)]) for r in range(h)])

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 21, 8)
