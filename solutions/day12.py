from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter
from collections import deque
from functools import partial
from statistics import median

"""
[Day 12 Results]
  Part 1
    > time:
    > rank:
  Part 2
    > time:
    > rank:
"""

day = 12

def parseLines(lines):
    graph = defaultdict(list)
    for line in lines:
        s, d = line.split('-')
        if d != "start" and s != "end":
            graph[s].append(d)
        if s != "start" and d != "end":
            graph[d].append(s)
    return graph

def numPaths(graph, curr, thisPath):
    childPaths = 0
    for n in graph[curr]:
        if n == "end":
            childPaths += 1
        elif n not in thisPath or n.isupper():
            childPaths += numPaths(graph, n, thisPath + [n])
    return childPaths

def numPathsB(graph, curr, path, secondSmall):
    childPaths = 0
    for n in graph[curr]:
        if n == "end":
            childPaths += 1
        elif n not in path or n.isupper():
            childPaths += numPathsB(graph, n, path + [n], secondSmall)
        elif not secondSmall:
            childPaths += numPathsB(graph, n, path + [n], True)
    return childPaths

# BFS here with all paths will help us keep track of path info.
def numPathsIter(g):
    togo = deque([["start"]])
    numPaths = 0
    while len(togo) > 0:
        nextPath = togo.pop()
        for edge in g[nextPath[-1]]:
            if edge == "end":
                numPaths += 1
            elif edge not in nextPath or edge.isupper():
                togo.appendleft(nextPath + [edge])
    return numPaths


def solveA(lines):
    # return numPaths(parseLines(lines), "start", [])
    return numPathsIter(parseLines(lines))

def solveB(lines):
    return numPathsB(parseLines(lines), "start", [], False)

answerAndSubmit(day, solveA, solveB, 10, 36)
