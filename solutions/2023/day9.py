from aoc_util import *

import numpy as np
import regex
from collections import defaultdict
from math import inf, prod

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  9   00:10:57    1487      0   00:13:57    1285      0
"""

day = 9

def parseInput(lines):
    return [[int(i) for i in h.split()] for h in lines]


def nextInSeq(hist):
    if all([h == 0 for h in hist]):
        return 0
    next = []
    for i in range(len(hist)-1):
        next.append(hist[i+1] - hist[i])
    return hist[-1] + nextInSeq(next)


def solveA(lines):
    histories = parseInput(lines)
    return sum([nextInSeq(h) for h in histories])


def firstInSeq(hist):
    if all([h == 0 for h in hist]):
        return 0
    next = []
    for i in range(len(hist)-1):
        next.append(hist[i+1] - hist[i])
    return hist[0] - firstInSeq(next)


def solveB(lines):
    histories = parseInput(lines)
    return sum([firstInSeq(h) for h in histories])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 114, 2)
