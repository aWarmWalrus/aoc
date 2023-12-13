from collections import defaultdict, deque
from heapq import heappop, heappush
import numpy as np
import math

# If the input is a list of lines that are equal length and to be treated as a
# grid, then this turns the input into a 2D numpy matrix with string dtype.
def createNumpy2D(lines, dtype=str, transformFn=None):
    h, w = len(lines), len(lines[0])
    mat = np.zeros((h,w), dtype=dtype)
    for (r, c) in np.ndindex(h, w):
        if transformFn == None:
            mat[r,c] = lines[r][c]
        else:
            mat[r,c] = transformFn(lines[r][c])
    return mat


# Returns a list of tuples representing the coordinates in np2dMatrix that match
# `val`
def findNumpyValue(np2dMatrix, val):
    ind = np.argwhere(np2dMatrix == val)
    return [tuple(i) for i in ind]


# Manhattan Distance
def manDist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Euclidean distance (as the crow flies)
def euclDist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def fourDirs():
    for d in [(-1,0), (0,-1), (1,0), (0,1)]:
        yield d


def eightDirs():
    for d in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0), (1,1)]:
        yield d


# validNeighbors() generates the valid neighbors for a given `coord` in the
# numpy 2D matrix. Can choose between four directions and eight directions.
# yields both the direction of travel and the new coordinate.
def validNeighbors(np2DMatrix, coord, dirFn=fourDirs):
    for d in dirFn():
        maxR, maxC = np2DMatrix.shape
        newR, newC = (coord[0] + d[0], coord[1] + d[1])
        if newC >= maxC  or newC < 0 or newR >= maxR or newR < 0:
            continue
        yield (newR, newC), d


# aStar() performs A* search on a numpy grid, returning the path from
# start to end, including start and end.
#
# Params:
# `canTraverseFn` should accept params (src and dst), and return true if can
#              traverse from src to dst.
# `distFn` should accept two params which are coordinates.
# `neighbors` is a generator that returns which points can be traveled to.
def aStar(grid, start, end, canTraverseFn, distFn=manDist, neighbors=fourDirs):
    # gScore is the cost of the cheapest known path from start to each node.
    stepsTo = defaultdict(lambda: math.inf)
    stepsTo[start] = 0

    cameFrom = defaultdict()
    togo = [(distFn(start, end), start)]
    while len(togo) > 0:
        cost, curr = heappop(togo)
        steps = stepsTo[curr]

        # Reached the goal
        if curr == end:
            path = deque(end)
            while curr != start:
                path.appendleft(curr)
                curr = cameFrom[curr]
            return path

        for next, _ in validNeighbors(grid, curr, dirFn=neighbors):
            if not canTraverseFn(curr, next):
                continue

            if steps + 1 < stepsTo[next]:
                stepsTo[next] = steps + 1
                cameFrom[next] = curr
                # fScore is our best guess as to how cheap a path could be from
                # start to finish if it goes through this node.
                fScore = steps + distFn(next, end)
                heappush(togo, (fScore, next))

    # No paths lead from start to end
    return None
