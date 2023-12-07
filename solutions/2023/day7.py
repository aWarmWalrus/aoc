from aoc_util import *

import numpy as np
import regex
from collections import defaultdict, Counter
from functools import cmp_to_key

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  7   00:32:19    2898      0   00:42:56    2047      0
"""

day = 7

def parseInput(lines):
    hands = []
    for l in lines:
        hands.append((l.split()[0], int(l.split()[1])))
    return hands


def handType(h):
    c = Counter(h)
    maxCount = max(c.values())
    isFullHouse = (maxCount == 3) and (2 in c.values())
    values = sorted(c.values())
    isTwoPair = len(values) == 3 and values[2] == 2 and values[1] == 2
    if maxCount == 5:
        return 6
    if maxCount == 4:
        return 5
    if isFullHouse:
        return 4
    if maxCount == 3:
        return 3
    if isTwoPair:   # Two pair
        return 2
    if maxCount == 2:
        return 1
    # High card
    return 0


def cardValue(c):
    values = {
        '2': 0,
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        'T': 8,
        'J': 9,
        'Q': 10,
        'K': 11,
        'A': 12,
    }
    return values[c]


def compareHands(h1b, h2b):
    h1 = h1b[0]
    h2 = h2b[0]
    if handType(h1) == handType(h2):
        for i in range(len(h1)):
            if cardValue(h1[i]) == cardValue(h2[i]):
                continue
            return 1 if cardValue(h1[i]) > cardValue(h2[i]) else -1
        return 0
    return 1 if handType(h1) > handType(h2) else -1


def solveA(lines):
    hands = parseInput(lines)
    ranked = sorted(hands, key=cmp_to_key(compareHands))
    return sum([(rank+1) * ranked[rank][1] for rank in range(len(ranked))])


def cardValueB(c):
    values = {
        '2': 0,
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        'T': 8,
        'J': -1,
        'Q': 10,
        'K': 11,
        'A': 12,
    }
    return values[c]

    
memo = defaultdict(str)

def maxHand(h):
    if h in memo.keys():
        return memo[h]
    if 'J' not in h:
        memo[h] = handType(h)
        return handType(h)
    bestType = 0
    for c in range(len(h)):
        if h[c] == 'J':
            for p in '23456789TQKA':
                newH = h[0:c] + p + h[c+1:]
                newType = maxHand(newH)
                if newType > bestType:
                    bestType = newType
    memo[h] = bestType
    return bestType


def compareHandsB(h1b, h2b):
    h1 = h1b[0]
    h2 = h2b[0]
    if maxHand(h1) == maxHand(h2):
        for i in range(len(h1)):
            if cardValueB(h1[i]) == cardValueB(h2[i]):
                continue
            return 1 if cardValueB(h1[i]) > cardValueB(h2[i]) else -1
        return 0
    return 1 if maxHand(h1) > maxHand(h2) else -1


def solveB(lines):
    hands = parseInput(lines)
    hs = sorted(hands, key=cmp_to_key(compareHandsB))
    rank = 1
    acc = 0
    for h in hs:
        acc += rank * h[1]
        rank += 1
    return acc


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 6440, 5905)
