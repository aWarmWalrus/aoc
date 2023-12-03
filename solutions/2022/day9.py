from aoc_util import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  9       >24h   54612      0       >24h   45443      0
"""

day = 9

def updateHead(pos, dir):
    if dir == "L":
        return (pos[0]-1, pos[1])
    elif dir == "R":
        return (pos[0]+1, pos[1])
    elif dir == "U":
        return (pos[0], pos[1]+1)
    elif dir == "D":
        return (pos[0], pos[1]-1)
    else:
        panic("Unexpected direction", dir)

def manhattanDist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def longestSingle(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def updateTail(pos, head):
    kern = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    if longestSingle(pos,head) <= 1:
        return pos
    closest = pos
    shortest = manhattanDist(pos,head)
    for k in kern:
        newPos = (pos[0]+k[0], pos[1]+k[1])
        if manhattanDist(newPos, head) < shortest:
            shortest = manhattanDist(newPos, head)
            closest = newPos
    return closest

def solveA(lines):
    h, t = (0, 0), (0, 0)
    tHist = set({t})
    for l in lines:
        dir, num = l.split()
        for n in range(int(num)):
            h = updateHead(h, dir)
            t = updateTail(t, h)
            tHist.add(t)
    return len(tHist)

def solveB(lines):
    segments = 10
    rope = [(0,0) for i in range(segments)]
    tHist = set({(0,0)})
    for l in lines:
        dir, dis = l.split()
        for n in range(int(dis)):
            rope[0] = updateHead(rope[0], dir)
            for i in range(1, segments):
                rope[i] = updateTail(rope[i], rope[i-1])
            tHist.add(rope[segments-1])
    return len(tHist)

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 13, 1)
