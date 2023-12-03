from aoc_util import *

import numpy as np
from math import prod
from collections import defaultdict

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  3       >24h              0       >24h              0
"""

day = 3

def convert(lines):
    sch = np.zeros((len(lines), len(lines[0])), dtype=str)
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            sch[r, c] = lines[r][c]
    return sch


# Returns the number and length iff [r,c] is the first digit of the number.
def getNumber(map, r, c):
    if not map[r,c].isdigit():
        return None

    if c == 0 or not map[r, c-1].isdigit():
        if c + 1 < map.shape[0] and map[r, c+1].isdigit():
            if c + 2 < map.shape[1] and map[r, c+2].isdigit():
                return map[r, c] + map[r, c+1] + map[r, c+2]
            else:
                return map[r, c] + map[r, c+1]
        else:
            return map[r, c]

    return None


def solveA(lines):

    def hasAdjacentSymbol(map, number, r, c):
        maxR = map.shape[0]
        maxC = map.shape[1]
        chars = map[max(0, r-1) : min(maxR, r+2), max(0, c-1) : min(maxC, c+1+len(number))].flatten()
        return any([not v.isdigit() and v != "." for v in chars])

    sum = 0
    scheme = convert(lines)
    for r in range(scheme.shape[0]):
        for c in range(scheme.shape[1]):
            number = getNumber(scheme, r, c)
            if number is None:
                continue
            if hasAdjacentSymbol(scheme, number, r, c):
                sum += int(number)

    return sum


def solveB(lines):

    def getUniqueAdjNumbers(map, knowns, r, c):
        neighbors = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        uniques = set()
        for (rd, cd) in neighbors:
            row = r + rd
            col = c + cd
            if row < 0 or row > map.shape[0] or col < 0 or col > map.shape[1]:
                continue
            if map[row, col].isdigit():
                uniques.add(knowns[(row, col)])
        return uniques


    scheme = convert(lines)

    id = 0
    knownNumbers = defaultdict()
    for r in range(scheme.shape[0]):
        for c in range(scheme.shape[1]):
            number = getNumber(scheme, r, c)
            if number is None:
                continue
            for i in range(len(number)):
                knownNumbers[(r,c+i)] = (number, id)
            id += 1

    sum = 0
    for r in range(scheme.shape[0]):
        for c in range(scheme.shape[1]):
            if scheme[r, c] == "*":
                uniques = getUniqueAdjNumbers(scheme, knownNumbers, r, c)
                if len(uniques) != 2:
                    continue
                ratio = prod([int(u[0]) for u in uniques])
                sum += ratio

    return sum


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 4361, 467835)
