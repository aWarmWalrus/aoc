from aoc_util import *
from aoc_algos import *

from collections import deque
import numpy as np
import time
from z3 import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 24   00:40:48     888      0   23:12:21    6349      0
"""

day = 24

def parseInput(lines):
    hails = []
    for l in lines:
        px, py, pz = [int(i) for i in l.split('@')[0].split(',')]
        vx, vy, vz = [int(i) for i in l.split('@')[1].split(',')]
        hails.append(((px,py,pz),(vx,vy,vz)))

    return hails


def unit(coord):
    dir = coord / np.linalg.norm(coord)
    return dir


def intersect(h1, h2):
    m1 = h1[1][2] / h1[1][1]
    m2 = h1[2][2] / h1[2][1]


def solveA(lines):
    hails = parseInput(lines)
    minX, maxX = (7, 27) if len(hails) < 10 else (200000000000000, 400000000000000)
    minY, maxY = (7, 27) if len(hails) < 10 else (200000000000000, 400000000000000)
    total = 0
    for i in range(len(hails)):
        x1, y1= hails[i][0][0:2]
        vx1, vy1= hails[i][1][0:2]
        m1 = vy1 / vx1
        for j in range(i+1, len(hails)):
            x2, y2 = hails[j][0][0:2]
            vx2, vy2 = hails[j][1][0:2]
            m2 = vy2 / vx2
            if (m1 - m2) == 0:
                continue

            # Has to meet within bounds
            x = ((y2 - y1) + m1 * x1 - m2 * x2) / (m1 - m2)
            y = m1 * (x - x1) + y1
            if x < minX or x > maxX or y < minY or y > maxY:
                continue
            # AND has to meet in the future, not in the past
            t1 = (x - x1) / vx1
            t2 = (x - x2) / vx2
            if t1 > 0 and t2 > 0:
                total += 1
    return total


def solveB(lines):
    hails = parseInput(lines)
    total = 0
    x, y, z, vx, vy, vz, t1, t2, t3 = Ints('x y z vx vy vz t1 t2 t3')
    (x1, y1, z1), (vx1, vy1, vz1) = hails[0]
    (x2, y2, z2), (vx2, vy2, vz2) = hails[1]
    (x3, y3, z3), (vx3, vy3, vz3) = hails[2]
    s = Solver()
    s.add(x + vx * t1 == x1 + vx1 * t1)
    s.add(x + vx * t2 == x2 + vx2 * t2)
    s.add(x + vx * t3 == x3 + vx3 * t3)

    s.add(y + vy * t1 == y1 + vy1 * t1)
    s.add(y + vy * t2 == y2 + vy2 * t2)
    s.add(y + vy * t3 == y3 + vy3 * t3)

    s.add(z + vz * t1 == z1 + vz1 * t1)
    s.add(z + vz * t2 == z2 + vz2 * t2)
    s.add(z + vz * t3 == z3 + vz3 * t3)

    s.add(t1 > 0, t2 > 0, t3 > 0)
    s.check()
    m = s.model()
    print(s.model())

    return m.evaluate(x+y+z)


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 2, 47)
