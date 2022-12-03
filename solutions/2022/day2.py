from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  2       >24h  121878      0       >24h  115882      0
"""

day = 2

def solveA(lines):
    cVal = {
        "A X": 3,
        "A Y": 6,
        "A Z": 0,
        "B X": 0,
        "B Y": 3,
        "B Z": 6,
        "C X": 6,
        "C Y": 0,
        "C Z": 3,
    }
    tVal = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    return sum([cVal[l] + tVal[l.split()[1]] for l in lines])

def solveB(lines):
    cVal = {
        "A X": 3,
        "A Y": 1,
        "A Z": 2,
        "B X": 1,
        "B Y": 2,
        "B Z": 3,
        "C X": 2,
        "C Y": 3,
        "C Z": 1,
    }
    tVal = {
        "X": 0,
        "Y": 3,
        "Z": 6,
    }
    return sum([cVal[l] + tVal[l.split()[1]] for l in lines])

answerAndSubmit(day, solveA, solveB, 15, 12)
