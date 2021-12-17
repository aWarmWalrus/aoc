import math
from bitstring import BitArray
import aoc_util
from aoc_util import *

"""
[Day 17 Results]
  Part 1
    > time: 00:48:44
    > rank: 1225
  Part 2
    > time: 01:00:09
    > rank: 1068
"""
day = 17

aoc_util.PRINT_DEBUG = True

def targetArea(lines):
    _, _, xStr, yStr = lines[0].split()
    xi, xf = xStr.strip('x=,').split("..")
    yi, yf = yStr.strip('y=,').split("..")
    return ((int(xi), int(xf)), (int(yi), int(yf)))

def inTarget(p, target):
    tx = target[0]
    ty = target[1]
    return p[0] >= tx[0] and p[0] <= tx[1] and p[1] >= ty[0] and p[1] <= ty[1]

def pastTarget(p, target):
    tx = target[0]
    ty = target[1]
    return p[0] > tx[1] or (p[1] < ty[1] and p[1] < ty[0])

def simulate(vi, target, steps=100):
    heights = []
    p = (0,0)
    for i in range(steps):
        heights.append(p[1])
        p = (p[0] + vi[0], p[1] + vi[1])
        vi = (vi[0] - 1 if vi[0] > 0 else 0, vi[1] - 1)
        if inTarget(p, target):
            return True, max(heights)
        if pastTarget(p, target):
            return False, max(heights)
    return False, max(heights)

def solveA(lines, optimal=False):
    target = targetArea(lines)
    maxHeight = 0
    bestV = (0,0)
    for vx in range(50):
        for vy in range(300):
            hit, height = simulate((vx,vy), target, 500)
            if hit and height > maxHeight:
                bestV = (vx, vy)
                maxHeight = height
    debug("Best velocity: {}".format(bestV))
    return maxHeight

def solveB(lines, optimize=True):
    target = targetArea(lines)
    hits = 0
    bestV = (0,0)
    for vx in range(200):
        for vy in range(-500, 500):
            hit, height = simulate((vx,vy), target, 600)
            if hit:
                debug("{}".format((vx,vy)))
                hits += 1
    return hits

answerAndSubmit(day, solveA, solveB, 45, 112)
