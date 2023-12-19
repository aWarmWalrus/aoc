from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 17   23:11:04   15279      0   23:49:40   14233      0
"""

day = 17

def parseInput(lines):
    map = createNumpy2D(lines, dtype=int)
    return map


def dirName(dir):
    return {
        (1,0): "v",
        (-1,0): "^",
        (0,1): ">",
        (0,-1): "<",
    }[dir]


def aStarM(grid, start, end, distFn=manDist, neighbors=fourDirs):
    costs = defaultdict(lambda: math.inf)

    cameFrom = defaultdict()
    togo = []
    for next, dir in validNeighbors(grid, start, dirFn=neighbors):
        fScore = grid[next] + distFn(next, end)
        node = (next, dir, 1)
        togo.append((fScore, node))
        cameFrom[node] = (start, None, 0)
        costs[node] = grid[next]

    while len(togo) > 0:
        fScore, node = heappop(togo)
        curr, dir, sameDir = node

        for next, ndir in validNeighbors(grid, curr, dirFn=neighbors):
            if (sameDir == 3 and dir == ndir) or dir == (-ndir[0], -ndir[1]):
                continue

            nCost = costs[node]
            nextCost = nCost + grid[next]
            dirCount = 1 if ndir != dir else (sameDir + 1)
            nNode = (next, ndir, dirCount)

            if nextCost < costs[nNode]:
                costs[nNode] = nextCost
                cameFrom[nNode] = node
                # fScore is our best guess as to how cheap a path could be from
                # start to finish if it goes through this node.
                fScore = nextCost + distFn(next, end)
                heappush(togo, (fScore, nNode))

    # Assume we reach the end.
    path = deque()
    best = math.inf
    bestEnd = None
    for i in range(3):
        endRight = (end, (0,1), i+1)
        cost = costs[endRight]
        if cost < best:
            best = cost
            bestEnd = endRight
        endDown= (end, (1,0), i+1)
        cost = costs[endDown]
        if cost < best:
            best = cost
            bestEnd = endDown

    curr = bestEnd
    while curr[0] != start:
        path.appendleft(curr[0])
        curr = cameFrom[curr]
    return path


def solveA(lines):
    map = parseInput(lines)
    print(map)
    end = (map.shape[0]-1, map.shape[1]-1)
    total = 0
    path = aStarM(map, (0,0), end)
    return sum([map[coord] for coord in path])


def aStarM2(grid, start, end, distFn=manDist, neighbors=fourDirs):
    costs = defaultdict(lambda: math.inf)

    cameFrom = defaultdict()
    # togo = []
    # for next, dir in validNeighbors(grid, start, dirFn=neighbors):
    #     cNode = (start, None, 0)
    #     accCost = 0
    #     for i in range(10):
    #         accCost += grid[next]
    #         nextNode = (next, dir, i+1)
    #
    #         if i >= 3 and accCost < costs[nextNode]:
    #             costs[nextNode] = accCost
    #             cameFrom[nextNode] = cNode
    #             fScore = accCost + distFn(next, end)
    #             heappush(togo, (fScore, nextNode))
    #             cNode = nextNode
    #         next = (next[0] + dir[0], next[1] + dir[1])
    #         if isOob(grid, next):
    #             break

    togo = [(distFn(start, end), (start, None, 0))]
    while len(togo) > 0:
        fScore, node = heappop(togo)
        curr, dir, sameDir = node

        for next, ndir in validNeighbors(grid, curr, dirFn=neighbors):
            # Don't go forward or backwards, only left or right.
            if dir == ndir or dir == (-ndir[0], -ndir[1]):
                continue

            cNode = node
            accCost = costs[cNode]
            for i in range(10):
                accCost += grid[next]
                nextNode = (next, ndir, i+1)

                if i >= 3 and accCost < costs[nextNode]:
                    costs[nextNode] = accCost
                    cameFrom[nextNode] = cNode
                    # fScore is our best guess as to how cheap a path could be from
                    # start to finish if it goes through this node.
                    fScore = accCost + distFn(next, end)
                    heappush(togo, (fScore, nextNode))
                    cNode = nextNode
                next = (next[0] + ndir[0], next[1] + ndir[1])
                if isOob(grid, next):
                    break

    # Assume we reach the end.
    path = deque()
    best = math.inf
    bestEnd = None
    for i in range(4, 11):
        endRight = (end, (0,1), i)
        cost = costs[endRight]
        if cost < best:
            best = cost
            bestEnd = endRight
        endDown= (end, (1,0), i)
        cost = costs[endDown]
        if cost < best:
            best = cost
            bestEnd = endDown

    curr = bestEnd
    while curr[0] != start:
        path.appendleft(curr[0])
        curr = cameFrom[curr]
    return best


def solveB(lines):
    map = parseInput(lines)
    end = (map.shape[0]-1, map.shape[1]-1)
    total = 0
    return aStarM2(map, (0,0), end)


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 102, 94)
