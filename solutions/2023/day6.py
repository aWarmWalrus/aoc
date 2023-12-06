from aoc_util import *

import numpy as np
import regex
from collections import defaultdict
from math import inf, prod

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  6   00:05:30     658      0   00:08:05     614      0
"""

day = 6

def parseInput(lines):
    times = [int(i) for i in lines[0].split()[1:]]
    distances = [int(i) for i in lines[1].split()[1:]]
    races = [(times[i], distances[i]) for i in range(len(times))]
    return races


def parseInput2(lines):
    time = int("".join(lines[0].split()[1:]))
    dist = int("".join(lines[1].split()[1:]))
    return time, dist


def solveA(lines):
    races = parseInput(lines)
    # acc = 1
    # for r in races:
    #     wins = 0
    #     bestDistance = r[1]
    #     time = r[0]
    #     for millis in range(r[0]):
    #         dist = (timeAllowed - millis) * millis
    #         if dist > bestDistance:
    #             wins += 1
    #     acc *= sum([1 if (r[0] - m) * m > r[1] else 0 for m in range(r[0])])
    # return acc
    return prod( [ sum( [1 if (r[0] - m) * m > r[1] else 0 for m in range(r[0])] ) for r in races] )


def solveB(lines):
    time, dist = parseInput2(lines)
    # wins = 0
    # for millis in range(time):
    #     distTraveled = (time - millis) * millis
    #     if distTraveled > dist:
    #         wins += 1
    # return wins
    return sum([1 if (time - m) * m > dist else 0 for m in range(time)])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 288, 71503)
