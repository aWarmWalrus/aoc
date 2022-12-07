from aoc_util import *

from collections import deque

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  6   00:04:56    1962      0   00:06:01    1798      0
"""

day = 6

def allUnique(wrd, length):
    if len(wrd) != length:
        return False
    other = ""
    for c in wrd:
        if c in other:
            return False
        other += c
    return True

def findStart(message, length):
    for i in range(len(message)):
        st = max(0, i - length)
        if allUnique(message[st:i], length):
            return i
    return 0

def solveA(lines):
    return findStart(lines[0], 4)

def solveB(lines):
    return findStart(lines[0], 14)

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 7, 19)
