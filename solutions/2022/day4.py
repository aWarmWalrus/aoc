from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  4   00:13:04    6227      0   00:20:09    6767      0
"""

day = 4

def solveA(lines):
    tot = 0
    for l in lines:
        p1, p2 = l.split(',')
        p1a, p1b = map(int, p1.split('-'))
        p2a, p2b = map(int, p2.split('-'))
        if (p1a >= p2a and p1b <= p2b) or (p2a >= p1a and p2b <= p1b):
            tot += 1
    return tot

def solveB(lines):
    tot = 0
    for l in lines:
        p1, p2 = l.split(',')
        p1a, p1b = map(int, p1.split('-'))
        p2a, p2b = map(int, p2.split('-'))
        if (p2a <= p1b and p2a >= p1a) or (p1a >= p2a and p1a <= p2b):
            tot += 1
    return tot

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 3, 5)
