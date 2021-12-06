from aoc_util import *
from collections import defaultdict
import numpy as np

"""
[Day 6 Results]
  Part 1
    > time: 00:28:48
    > rank: 8264
  Part 2
    > time: 00:29:56
    > rank: 3523
"""

day = 6

def solveA(lines, days=80):
    state = defaultdict(int)
    for i in list(map(int, lines[0].split(','))):
        state[i] += 1
    for _ in range(days):
        newState = defaultdict(int)
        for k, v in state.items():
            if (k == 0):
                newState[8] += v
                newState[6] += v
            else:
                newState[k-1] += v
        state = newState
    return sum(state.values())

def solveB(lines):
    return solveA(lines, 256)

answer(solveA, getInput(day), getTestInput(day), 5934, True)
answer(solveB, getInput(day), getTestInput(day), 26984457539, True)
