from aoc_util import *

import numpy as np
import regex
from collections import defaultdict
from math import inf, prod

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  8   00:09:32    2100      0   00:35:03    2224      0
"""

day = 8

def parseInput(lines):
    inst = lines[0]
    nodes = {}
    for l in lines[2:]:
        node = l.split()[0]
        lN = l[7:10]
        lR = l[12:15]
        nodes[node] = (lN, lR)
    return inst, nodes


def solveA(lines):
    inst, nodes = parseInput(lines)
    curr = "AAA"
    steps = 0
    while curr != "ZZZ":
        curr = nodes[curr][0] if inst[steps % len(inst)] == "L" else nodes[curr][1]
        steps += 1
    return steps


def returnA(lines):
    return 6


def solveB(lines):
    inst, nodes = parseInput(lines)
    steps = 0
    ghosts = []
    stepsToEnd= []
    for n in nodes.keys():
        if n[2] == 'A':
            ghosts.append(n)
    steps = 0
    while len(stepsToEnd) < len(ghosts):
        newGhosts = []
        for g in ghosts:
            nextInst = inst[steps % len(inst)]
            newGhosts.append(nodes[g][0] if nextInst == 'L' else nodes[g][1])

        # Each ghost will see their 'XXZ' exactly once before any sees it
        # for the second time.
        if any([g[2] == 'Z' for g in ghosts]):
            stepsToEnd.append(steps)
            print(steps, int(steps / len(inst)), ghosts)
        ghosts = newGhosts
        steps += 1

    return np.lcm.reduce(stepsToEnd, dtype='int64')


if __name__ == "__main__":
    answerAndSubmit(day, returnA, solveB, 6, 6)
