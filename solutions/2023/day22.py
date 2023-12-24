from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time
import math

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 22       >24h   12797      0       >24h   12339      0
"""

day = 22

class Coordinate:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]

    def modifyZ(self, amt):
        self.z += amt

    def distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)

class Brick:
    def __init__(self, id, front, back):
        self.id = id
        self.front = front
        self.back = back

    def lowerBy(self, amt):
        f = self.front
        b = self.back
        self.front.modifyZ(-amt)
        self.back.modifyZ(-amt)

    def blocks(self):
        blocks = []
        if self.front.x != self.back.x:
            assert self.front.z == self.back.z and self.front.y == self.back.y
            for x in range(self.front.x, self.back.x+1):
                blocks.append((x, self.front.y, self.front.z))
        elif self.front.y != self.back.y:
            assert self.front.z == self.back.z and self.front.x == self.back.x
            for y in range(self.front.y, self.back.y+1):
                blocks.append((self.front.x, y, self.front.z))
        elif self.front.z != self.back.z:
            assert self.front.x == self.back.x and self.front.y == self.back.y
            for z in range(self.front.z, self.back.z+1):
                blocks.append((self.front.x, self.front.y, z))
        else:
            assert self.front.x == self.back.x and self.front.y == self.back.y and self.front.z == self.back.z
            blocks.append((self.front.x, self.front.y, self.front.z))

        return blocks


    def horizontalProfile(self):
        xys = []
        if self.front.z != self.back.z:
            assert self.front.x == self.back.x and self.front.y == self.back.y
            return [(self.front.x, self.front.y)]
        elif self.front.x != self.back.x:
            for x in range(self.front.x, self.back.x+1):
                xys.append((x, self.front.y))
        elif self.front.y != self.back.y:
            for y in range(self.front.y, self.back.y+1):
                xys.append((self.front.x, y))
        else:
            xys.append((self.front.x, self.front.y))
        return xys

    def isRestingOn(self, other):
        # Assume self is higher than other.
        if min(self.front.z, self.back.z) != max(other.front.z, other.back.z) + 1:
            return False
        me = self.horizontalProfile()
        you = other.horizontalProfile()
        if len(set(me).intersection(you)) == 0:
            return False
        return True

    def supportedBy(self, bricks):
        sup = []
        for b in bricks:
            if b == self:
                continue
            if self.isRestingOn(b):
                sup.append(b)
        return sup

    def __str__(self):
        return "{}[{} {} {}]=[{} {} {}]".format(self.id, self.front.x, self.front.y, self.front.z, self.back.x, self.back.y, self.back.z)

    def __repr__(self):
        return str(self)


def parseInput(lines):
    bricks = []
    maxX, maxY, maxZ = 0, 0, 0
    id = 1
    for l in lines:
        f, b = l.split('~')
        front = Coordinate(tuple([int(i) for i in f.split(',')]))
        back = Coordinate(tuple([int(i) for i in b.split(',')]))
        bricks.append(Brick(id, front,back))
        maxX = max(maxX, front.x, back.x)
        maxY = max(maxY, front.y, back.y)
        maxZ = max(maxZ, front.z, back.z)
        id += 1

    space = np.zeros((maxX+1, maxY+1, maxZ+1), dtype=int)
    for b in bricks:
        # print(b)
        if b.front.x != b.back.x:
            for x in range(b.front.x, b.back.x+1):
                space[x, b.front.y, b.front.z] = b.id
        elif b.front.y != b.back.y:
            for y in range(b.front.y, b.back.y+1):
                space[b.front.x, y, b.front.z] = b.id
        elif b.front.z != b.back.z:
            for z in range(b.front.z, b.back.z+1):
                space[b.front.x, b.front.y, z] = b.id
        else:
            space[b.front.x, b.front.y, b.front.z] = b.id

    return space, sorted(bricks, key=lambda br: min(br.front.z, br.back.z))


def blockSupportedBy(space, brick):
    minZ = min(brick.front.z, brick.back.z)
    if minZ == 1:
        return [0] # supported by the ground lol
    assert minZ > 1
    supportedBy = []
    profile = brick.horizontalProfile()
    # unsupported = True
    for block in profile:
        under = (block[0], block[1], minZ-1)
        if space[under] != 0 and space[under] not in supportedBy:
            supportedBy.append(space[under])
            # unsupported = False
    return supportedBy


def collapseBricks(space, bricks):
    spCopy = np.copy(space)
    brCopy = bricks.copy()

    for i in range(len(brCopy)):
        brick = brCopy[i]
        bricksUnder = blockSupportedBy(spCopy, brick)
        while len(bricksUnder) == 0:
            minZ = min(brick.front.z, brick.back.z)
            for b in brick.blocks():
                spCopy[b] = 0
            brick.lowerBy(1)
            for b in brick.blocks():
                spCopy[b] = brick.id
            bricksUnder = blockSupportedBy(spCopy, brick)
    return spCopy, brCopy


def solveA(lines):
    space, bricks = parseInput(lines)
    space, bricks = collapseBricks(space, bricks)
    assert all([len(blockSupportedBy(space,b)) > 0 for b in bricks])

    bricks = sorted(bricks, key=lambda b: min(b.front.z, b.back.z), reverse=True)
    supports = defaultdict(list)
    for b in bricks:
        for brickUnder in blockSupportedBy(space, b):
            supports[brickUnder].append(b)

    total = 0
    for b in bricks:
        # A block that doesn't support anything can be removed.
        if len(supports[b.id]) == 0:
            total += 1
            continue
        canDisintegrate = True
        for other in supports[b.id]:
            if len(blockSupportedBy(space, other)) == 1:
                canDisintegrate = False
        if canDisintegrate:
            total += 1

    return total


# Returns the list of blocks that would fall if block bID is removed.
def wouldFall(supports, bID):
    supportsCopy = supports.copy()
    acc = set()
    falling = [bID]
    while len(falling) > 0:
        removed = falling.pop()
        # For every block that `removed` supports, count how many other blocks
        # (not including `removed`) support that block. If that list is empty,
        # then that block gets added to the falling queue.
        for above in supportsCopy[removed]:
            supportedBy = []
            for ob, supports in supportsCopy.items():
                if above in supports and ob != removed:
                    supportedBy.append(ob)
            if len(supportedBy) == 0:
                falling.append(above)
                acc.add(above)
        supportsCopy[removed] = []
    return acc


def solveB(lines):
    space, bricks = parseInput(lines)
    space, bricks = collapseBricks(space, bricks)
    assert all([len(blockSupportedBy(space,b)) > 0 for b in bricks])

    bricks = sorted(bricks, key=lambda b: min(b.front.z, b.back.z), reverse=True)
    supports = defaultdict(list)
    for b in bricks:
        for under in blockSupportedBy(space, b):
            supports[under].append(b.id)
    return sum([len(wouldFall(supports, b.id)) for b in bricks])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 5, 7)
