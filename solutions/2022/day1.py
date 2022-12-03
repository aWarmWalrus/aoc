from aoc_util import *

import heapq

"""
[Day 1 Results]
  Part 1
    > time:
    > rank:
  Part 2
    > time:
    > rank:
"""

day = 1

def solveA(lines):
    mostCals = 0
    currentCals = 0
    for l in lines:
        if len(l) == 0:
            if currentCals > mostCals:
                mostCals = currentCals
            currentCals = 0
            continue
        currentCals += int(l)

    return mostCals

def solveB(lines):
    cals = []
    currentCals = 0
    for l in lines:
        if len(l) == 0:
            cals += [currentCals]
            currentCals = 0
            continue
        currentCals += int(l)
    cals += [currentCals]
    cals = sorted(cals)

    return sum(cals[-3:])

answerAndSubmit(day, solveA, solveB, 24000, 45000)
