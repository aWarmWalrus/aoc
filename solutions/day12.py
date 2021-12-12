from aoc_util import *
import numpy as np
import cProfile
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


def solveA(lines, useRecursive = False):
    return numPaths(parseLines(lines), "start", []) if useRecursive else numPathsIter(parseLines(lines))

def solveB(lines):
    return numPathsB(parseLines(lines), "start", [], False)

answerAndSubmit(day, solveA, solveB, 10, 36)

input = getInput(day)
times = 100

debug("PROFILING: Iterative path-preserving BFS solution")
pr1 = cProfile.Profile()
pr1.enable()
for i in range(times):
    numPathsIter(parseLines(input))
pr1.disable()
pr1.print_stats(sort="time")

debug("PROFILING: Recursive path-preserving DFS solution")
pr2 = cProfile.Profile()
pr2.enable()
for i in range(times):
    numPaths(parseLines(input), "start", [])
pr2.disable()

pr2.print_stats(sort="time")
