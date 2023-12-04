from aoc_util import *

import regex
from collections import defaultdict

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  4   00:09:48    3068      0   00:19:14    2029      0
"""

day = 4

def parseCard(line):
    expr = r'Card\s+(\d+):\s+((?:\d+\s*)+)\s\|\s+((?:\d+\s*)+)\s*'
    cID, w, n = regex.findall(expr, line)[0]
    wins = [int(i) for i in w.split()]
    nums = [int(i) for i in n.split()]
    return cID, wins, nums


def solveA(lines):
    total = 0
    for line in lines:
        _, wins, nums = parseCard(line)
        numWins = sum([(1 if n in wins else 0) for n in nums])
        if numWins == 0:
            continue
        total += 2 ** (numWins - 1)
    return total


def solveB(lines):
    total = 0
    # Count the original card as a copy, so we have at least 1 of every card.
    copies = defaultdict(lambda: 1)
    for line in lines:
        cID, wins, nums = parseCard(line)
        total += copies[int(cID)]
        numWins = sum([(1 if n in wins else 0) for n in nums])
        for i in range(numWins):
            copies[int(cID) + i + 1] += copies[int(cID)]
    return total


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 13, 30)
