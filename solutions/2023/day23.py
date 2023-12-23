from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time
import regex
import sys

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 23   00:25:34     952      0   02:13:58    1609      0
"""

day = 23


def parseInput(lines):
    array = createNumpy2D(lines, dtype=str)
    return array


def dfs(array, curr, end, path):
    # print(curr, path)
    # input()
    if curr == end:
        return path

    val = array[curr]
    if val in "<v^>":
        if val == "<":
            next = (curr[0], curr[1]-1)
        elif val == ">":
            next = (curr[0], curr[1]+1)
        elif val == "^":
            next = (curr[0]-1, curr[1])
        elif val == "v":
            next = (curr[0]+1, curr[1])
        return dfs(array, next, end, path + [curr])

    longestPath = []
    for next, dir in validNeighbors(array, curr):
        if array[next] == '#':
            continue
        if next in path:
            continue
        val = array[next]
        slopes = {
            ">": (0,1),
            "<": (0,-1),
            "^": (-1,0),
            "v": (1,0),
        }
        if val in "<>^v" and slopes[val] != dir:
            continue
        p = dfs(array, next, end, path+[curr])
        if len(p) > len(longestPath):
            longestPath = p
    return longestPath


def solveA(lines):
    sys.setrecursionlimit(10000)
    array = parseInput(lines)
    start = (0, 1)
    end = (array.shape[0]-1, array.shape[1]-2)
    path = dfs(array, start, end, [])
    return len(path)


class Vertex:
    def __init__(self, coord):
        self.neighbors = []
        self.coord = coord

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return other.coord == self.coord
        return False

    def __str__(self):
        acc = "["
        for n in self.neighbors[:-1]:
            acc += str(n[0].coord) + ":" + str(n[1]) + ","
        n = self.neighbors[-1]
        acc += str(n[0].coord) + ":" + str(n[1]) + "]"
        return "v" + str(self.coord) + "=>"+ acc

    def __repr__(self):
        return str(self)

def solveB(lines):
    array = parseInput(lines)
    start = (0, 1)
    end = (array.shape[0]-1, array.shape[1]-2)
    # for r,c in np.ndindex(array.shape):
    #     if array[r,c] in "<>v^":
    #         array[r,c] = '.'

    # Use DFS to collapse the grid into a graph of vertices and edges.
    vertices = {start: Vertex(start)}
    togo = deque([(start, vertices[start], 0, None)])
    while len(togo) > 0:
        curr, vert, pLen, prev = togo.pop()
        if curr == end:
            vEnd = Vertex(end)
            assert curr not in vertices
            vert.neighbors.append((vEnd, pLen))
            vEnd.neighbors.append((vert, pLen))
            continue
        neighbors = list(filter(lambda x: array[x[0]] != '#' and x[0] != prev, validNeighbors(array, curr)))
        assert len(neighbors) < 4
        if len(neighbors) == 1:
            togo.append((neighbors[0][0], vert, pLen+1, curr))
        elif len(neighbors) >= 2:
            # If I've seen curr (vertex) already, don't add its neighbors, since
            # they should have already been added the first time we saw curr.
            if curr in vertices:
                other = vertices[curr]
                if (vert, pLen+1) not in other.neighbors:
                    other.neighbors.append((vert, pLen+1))
                    vert.neighbors.append((other, pLen+1))
            else:
                # Else if curr is brand new, add all its neighbors
                newVert = Vertex(curr)
                newVert.neighbors.append((vert, pLen+1))
                vert.neighbors.append((newVert, pLen+1))
                vertices[curr] = newVert
                for n, _ in neighbors:
                    togo.append((n, newVert, 0, curr))
    for k, v in vertices.items():
        print("  ", k, v)

    togo = deque([(vertices[start],[], 0)])
    maxLength = 0
    pathsFound = 0
    while len(togo) > 0:
        curr, path, steps = togo.pop()
        if curr.coord == end:
            maxLength = max(steps, maxLength)
            pathsFound += 1
            continue
        for next, dist in curr.neighbors:
            if next.coord in path:
                continue
            togo.append((next, path+[curr.coord], steps + dist))

    print("Found {} paths".format(pathsFound))

    return maxLength


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 94, 154)
