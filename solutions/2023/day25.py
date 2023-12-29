from aoc_util import *
from aoc_algos import *

from collections import deque
import copy
import numpy as np
import time
from z3 import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 25       >24h   10794      0       >24h    7918      0
"""

day = 25

def parseInput(lines):
    wires = {}
    for l in lines:
        id = l.split(':')[0]
        components = l.split(':')[1].split()
        if id not in wires:
            wires[id] = []
        wires[id] += components
        for c in components:
            if c not in wires:
                wires[c] = []
            wires[c].append(id)
    return wires


def bfs(wires, start, end):
    togo = deque([(start, [])])
    visited = set()
    while len(togo) > 0:
        curr, path = togo.pop()
        if curr == end:
            return path
        visited.add(curr)
        for n in wires[curr]:
            if n not in visited:
                togo.append((n, path + [curr]))
    return None


def isMaxFlowOver(wires, start, end, maxFlow):
    residual = copy.deepcopy(wires)
    flow = 0
    while (path := bfs(residual, start, end)) is not None:
        if flow >= maxFlow:
            return True
        flow += 1
        dest = end
        for p in reversed(path):
            residual[p].remove(dest)
            residual[dest].remove(p)
            dest = p
    return False


def solveA(lines):
    wires = parseInput(lines)
    ingroup = set()
    outgroup = set()
    known = set()
    for start in wires.keys():
        if start in ingroup or start in outgroup:
            continue
        newIns = set([start])
        activeGroup = None
        for other in wires.keys():
            if other == start:
                continue
            if activeGroup is not None and (other in ingroup or other in outgroup):
                continue
            if isMaxFlowOver(wires, start, other, 3):
                if other in ingroup:
                    assert activeGroup is None
                    activeGroup = ingroup
                elif other in outgroup:
                    assert activeGroup is None
                    activeGroup = outgroup
                newIns.add(other)
        if activeGroup == None:
            activeGroup = ingroup if len(ingroup) <= len(outgroup) else outgroup
        for c in newIns:
            known.add(c)
            activeGroup.add(c)
        print("Start {}   total: {}   ins: {}   outs: {}".format(start, len(wires), len(ingroup), len(outgroup)))
        if len(ingroup) + len(outgroup) == len(wires):
            return len(ingroup) * len(outgroup)
    return None


def solveB(lines):
    wires = parseInput(lines)
    total = 0
    return total


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 54, 0)
