from aoc_util import *
import numpy as np
import cProfile
from collections import defaultdict
from collections import deque
from functools import partial

"""
[Day 13 Results]
  Part 1
    > time: 00:31:10
    > rank: 3417
  Part 2
    > time: 00:28:46
    > rank: 871
"""

day = 13

def parseLines(lines):
    instructions = []
    rowCoords = []
    colCoords = []
    for line in lines:
        if line.startswith("fold"):
            xyi = line.split()[2].split("=")
            instructions.append((xyi[0], int(xyi[1])))
        elif len(line) > 1:
            row,col = [int(i) for i in line.split(",")]
            rowCoords.append(row)
            colCoords.append(col)
    paper = np.zeros((max(rowCoords) + 1, max(colCoords) + 1), dtype=int)
    for c in zip(rowCoords, colCoords):
        paper[c[0], c[1]] = 1
    return paper, instructions

def doFolds(paper, instructions, numFolds):
    folds = 0
    for i in instructions:
        if folds == numFolds:
            break
        folds += 1
        if i[0] == "x":
            paper = paper[0:i[1]] | np.flip(paper[i[1]+1:], axis=0)
        elif i[0] == "y":
            paper = paper[:, 0:i[1]] | np.flip(paper[:, i[1]+1:], axis=1)
    return paper

def solveA(lines):
    paper, instructions = parseLines(lines)
    folded = doFolds(paper, instructions, 1)
    return folded.sum()

def solveB(lines):
    paper,instructions = parseLines(lines)
    folded = doFolds(paper, instructions, -1)
    for l in np.swapaxes(folded,0,1):
        debug("".join(["#" if i == 1 else " " for i in l]))

    return "FAGURZHE"

answerAndSubmit(day, solveA, solveB, 17, "FAGURZHE")
