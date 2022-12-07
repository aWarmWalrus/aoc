from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  3   00:28:30    9753      0   00:45:28    9873      0
"""

day = 3

def itemPriority(item):
    c = ord(item)
    if c >= ord('a'):
        return c - 96
    return c - 38

def solveA(lines):
    def getSharedItem(sack):
        mid = int(len(sack) / 2)
        return list(filter(lambda c: c in sack[mid:], sack[:mid]))[0]
    return sum([itemPriority(item) for item in map(getSharedItem, lines)])

def groupPriority(sacks):
    badge = list(filter(lambda c: (c in sacks[1] and c in sacks[2]), sacks[0]))[0]
    return itemPriority(badge)

def solveB(lines):
    return sum([groupPriority(lines[i:i+3]) for i in range(0, len(lines), 3)])

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 157, 70)
