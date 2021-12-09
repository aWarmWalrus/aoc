from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter

"""
[Day 9 Results]
  Part 1
    > time: 00:14:38
    > rank: 3126
  Part 2
    > time: 00:42:11
    > rank: 3202
"""

day = 9

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P({},{})".format(self.x, self.y)

    def __str__(self):
        return "P({},{})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def getAdjacent(x,y,map):
    xM = x-1
    xP = x+1
    yM = y-1
    yP = y+1
    adj = []
    if xM >= 0:
        adj.append( map[xM][y])
    if xP < len(map):
        adj.append(map[xP][y])
    if yM >= 0:
        adj.append(map[x][yM])
    if yP < len(map[0]):
        adj.append(map[x][yP])
    return adj

def solveA(lines):
    heatmap = []
    for line in lines:
        heatmap.append([int(i) for i in line])
    risk = 0
    for x in range(len(heatmap)):
        for y in range(len(heatmap[0])):
            lowest = True
            for i in getAdjacent(x,y,heatmap):
                if heatmap[x][y] >= i:
                    lowest = False
            if lowest:
                risk += heatmap[x][y] + 1
    return risk

def getAdj(point, map):
    xM = point.x-1
    xP = point.x+1
    yM = point.y-1
    yP = point.y+1
    adj = []
    if xM >= 0:
        adj.append(Point(xM,point.y))
    if xP < len(map):
        adj.append(Point(xP,point.y))
    if yM >= 0:
        adj.append(Point(point.x,yM))
    if yP < len(map[0]):
        adj.append(Point(point.x,yP))
    return adj

def solveB(lines):
    heatmap = []
    for line in lines:
        heatmap.append([int(i) for i in line])

    # Get the lowest points.
    lows = []
    for x in range(len(heatmap)):
        for y in range(len(heatmap[0])):
            lowest = True
            for i in getAdjacent(x,y,heatmap):
                if heatmap[x][y] >= i:
                    lowest = False
            if lowest:
                lows.append(Point(x,y))

    # basins is a map from a coordinate to the ID of the basin it is inside.
    basins = defaultdict(int)
    basinSizes = []
    for coord in lows:
        # do bfs until you see a 9 or an edge
        visited = [coord]
        goto = getAdj(coord, heatmap)  # start with the points adjacent.
        goto = list(filter(lambda p : heatmap[p.x][p.y] < 9, goto))
        while len(goto) > 0:
            next = goto.pop()
            visited.append(next)
            adj = getAdj(next, heatmap)
            adj = list(filter(lambda p : heatmap[p.x][p.y] < 9, adj))
            adj = list(filter(lambda p : p not in visited and p not in goto, adj))
            goto += adj

        basinSizes.append(len(visited))

    largest = sorted(basinSizes, reverse=True)[0:3]
    mul = 1
    for i in largest:
        mul *= i
    return mul

answerAndSubmit(day, solveA, solveB, 15,1134)
