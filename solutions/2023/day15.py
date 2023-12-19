from aoc_util import *
from aoc_algos import *

from collections import deque
import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 15   00:05:48    1631      0   00:28:30    1961      0
"""

day = 15

def parseInput(lines):
    return lines[0].split(',')


def hash(l):
    curr = 0
    for c in l:
        curr += ord(c)
        curr *= 17
        curr = (curr % 256)
    return curr


def solveA(lines):
    inp = parseInput(lines)
    return sum([hash(v) for v in inp])


def solveB(lines):
    inp = parseInput(lines)
    boxes = {}   # dict of box number (int) -> label (str)
    foci = {}    # dict of label (str) -> foci (int)
    for ins in inp:
        if '=' in ins:
            lab, foc = ins.split('=')
            box = hash(lab)
            if box not in boxes:
                boxes[box] = deque([lab])
                foci[lab] = int(foc)
                continue
            if lab not in boxes[box]:
                boxes[box].append(lab)
            foci[lab] = int(foc)

        elif '-' in ins:
            lab = ins[:-1]
            box = hash(lab)
            if box not in boxes or lab not in boxes[box]:
                continue
            boxes[box].remove(lab)
            del foci[lab]
    total = 0
    for box, ls in boxes.items():
        for lens in range(len(ls)):
            total += (box+1) * (lens+1) * foci[ls[lens]]
    return total


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 1320, 145)
