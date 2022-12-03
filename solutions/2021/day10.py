from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter
from functools import partial
from statistics import median

"""
[Day 10 Results]
  Part 1
    > time: 00:05:45
    > rank: 388
  Part 2
    > time: 00:13:51
    > rank: 688
"""

day = 10

OPENERS = ["[", "(", "<", "{"]
MATCHING = {")":"(", "]":"[", "}":"{", ">":"<"}

def solveA(lines):
    score = 0
    scoreMap = {")" : 3, "]" : 57, "}" : 1197, ">" : 25137}
    for line in lines:
        symStack = []
        for c in line:
            if c in OPENERS:
                symStack.append(c)
            elif symStack.pop() != MATCHING[c]:
                score += scoreMap[c]
                break
    return score

def solveB(lines):
    incompletes = []
    for line in lines:
        symStack = []
        corrupted = False
        for c in line:
            if c in OPENERS:
                symStack.append(c)
            elif symStack.pop() != MATCHING[c]:
                corrupted = True
                break
        if not corrupted:
            incompletes.append(symStack)

    scoreMap = {"(" : 1, "[" : 2, "{" : 3, "<" : 4}
    scores = []
    for symStack in incompletes:
        score = 0
        for c in reversed(symStack):
            score = score * 5 + scoreMap[c]
        scores.append(score)
    return median(scores)

answerAndSubmit(day, solveA, solveB, 26397, 288957)
