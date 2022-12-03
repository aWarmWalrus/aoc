from aoc_util import *

"""
[Day 3 Results]
  Part 1
    > time:
    > rank:
  Part 2
    > time:
    > rank:
"""

day = 3

def itemPriority(cha):
    if cha >= ord('a'):
        return cha - 96
    return cha - 38

def solveA(lines):
    total = 0
    for ruck in lines:
        mid = int(len(ruck) / 2)
        r1 = ruck[0:mid]
        r2 = ruck[mid:]
        shared = ""
        for c in r1:
            if c in r2:
                shared = c
                break
        # print("ruck 1: {}   ruck 2: {}    shared: {}".format(r1, r2, shared))
        total += itemPriority(ord(shared))
    print(total)
    return total

def priorOfGroup(ruck1, ruck2, ruck3):
    badge = ''
    for c in ruck1:
        if c in ruck2 and c in ruck3:
            badge = c
    return itemPriority(ord(badge))

def solveB(lines):
    total = 0
    for i in range(0, len(lines), 3):
        total += priorOfGroup(lines[i], lines[i+1], lines[i+2])
    return total

answerAndSubmit(day, solveA, solveB, 157, 70)
