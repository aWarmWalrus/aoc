import math
import copy
import ast
import json
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
day = 18

aoc_util.PRINT_DEBUG = False

class SnailfishNumber:
    def __init__(self, left, right):
        assert(type(left) == int or type(left) == SnailfishNumber)
        assert(type(right) == int or type(right) == SnailfishNumber)
        self.left = left
        self.right = right
        self.depth = 0
        self.parent = None
        self.side = None

    def addParent(self, parent, side):
        self.parent = parent
        self.side = side

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if type(self.left) == int:
            return "[{},{}]".format(self.left, self.right)
        else:
            return "[{},{}]".format(str(self.left), str(self.right))

    def __add__(self, other):
        sf = SnailfishNumber(self, other)
        self.addParent(sf, "left")
        other.addParent(sf, "right")
        while True:
            if sf.doExplode(0):
                debug("   Exploded! " + str(sf))
                continue
            if sf.doSplit():
                debug("   Split!    " + str(sf))
                continue
            break
        return sf

    def addDepth(self):
        self.depth += 1
        if (type(self.left) == SnailfishNumber):
            self.left.addDepth()
        if (type(self.right) == SnailfishNumber):
            self.right.addDepth()

    # Returns true if performing an addition would lead to an explosion.
    def willExplode(self):
        if self.depth == 3:
            return True
        elif type(self.left) == int:
            return False
        return self.left.willExplode() or self.right.willExplode()

    # Child calls this function to tell its parent to try add |incr| leftward.
    def addUpLeftward(self, incr, child):
        if child == "left":
            if self.parent is not None:
                self.parent.addUpLeftward(incr, self.side)
                return
            else:
                # Do nothing. No one is to the left.
                return
        elif child == "right":
            if type(self.left) == int:
                self.left += incr
            else:
                self.left.addDownRightward(incr)
            return
        raise Exception("Bad child: " + child)

    # Parent calls this function to tell it to add |incr| on the right side.
    def addDownRightward(self, incr):
        if type(self.right) == int:
            self.right += incr
        else:
            self.right.addDownRightward(incr)

    # Child calls this function to tell its parent to try add |incr| rightward.
    def addUpRightward(self, incr, child):
        if child == "right":
            if self.parent is not None:
                self.parent.addUpRightward(incr, self.side)
                return
            else:
                # Do nothing. No one is to the left.
                return
        elif child == "left":
            if type(self.right) == int:
                self.right += incr
            else:
                self.right.addDownLeftward(incr)
            return
        raise Error("Bad child: " + child)

    # Parent calls this function to tell it to add |incr| on the right side.
    def addDownLeftward(self, incr):
        if type(self.left) == int:
            self.left += incr
        else:
            self.left.addDownLeftward(incr)

    # Find the leftmost depth 0
    def doExplode(self, nested):
        if nested >= 3:
            if (type(self.left) == SnailfishNumber):
                # debug("     explode left node: " + str(self.left))
                assert(type(self.left.left) == int)
                assert(type(self.left.right) == int)
                self.parent.addUpLeftward(self.left.left, self.side)
                self.addUpRightward(self.left.right, "left")
                self.left = 0
                return True
            if (type(self.right) == SnailfishNumber):
                # debug("     explode right node: " + str(self.right))
                assert(type(self.right.left) == int)
                assert(type(self.right.right) == int)
                self.parent.addUpRightward(self.right.right, self.side)
                self.addUpLeftward(self.right.left, "right")
                self.right = 0
                return True
        # No explosion at this depth: go deeper.
        if (type(self.left) == SnailfishNumber):
            if self.left.doExplode(nested + 1):
                return True
        if (type(self.right) == SnailfishNumber):
            if self.right.doExplode(nested + 1):
                return True
        # No explosions left :)
        return False

    def doSplit(self):
        if (type(self.left) == int):
            if self.left > 9:
                lower = int(math.floor(self.left / 2))
                upper = int(math.ceil(self.left / 2))
                self.left = SnailfishNumber(lower, upper)
                self.left.addParent(self, "left")
                return True
        if (type(self.left) == SnailfishNumber):
            if self.left.doSplit():
                return True
        if (type(self.right) == int):
            if self.right > 9:
                lower = int(math.floor(self.right / 2))
                upper = int(math.ceil(self.right / 2))
                self.right = SnailfishNumber(lower, upper)
                self.right.addParent(self, "right")
                return True
        if (type(self.right) == SnailfishNumber):
            if self.right.doSplit():
                return True
        return False

    def magnitude(self):
        lMag = self.left if type(self.left) == int else self.left.magnitude()
        rMag = self.right if type(self.right) == int else self.right.magnitude()
        return 3 * lMag + 2 * rMag

def fromList(snailList):
    assert type(snailList) == list
    assert(len(snailList) == 2)
    left = snailList[0] if type(snailList[0]) == int else fromList(snailList[0])
    right = snailList[1] if type(snailList[1]) == int else fromList(snailList[1])
    parent = SnailfishNumber(left, right)
    if type(left) == SnailfishNumber:
        left.addParent(parent, "left")
    if type(right) == SnailfishNumber:
        right.addParent(parent, "right")
    return parent

def parseLines(lines):
    numbers = []
    for line in lines:
        snailStr = ast.literal_eval(line)
        numbers.append(fromList(snailStr))
    return numbers

def solveA(lines, optimal=False):
    numbers = parseLines(lines)
    sum = numbers[0]
    for i in range(1, len(numbers)):
        # debug("adding: \n   {}\n   {}".format(self, numbers[i]))
        sum = sum + numbers[i]
        # debug("SUM: " + str(sum))
    return sum.magnitude()

def solveB(lines, optimize=True):
    numbers = parseLines(lines)
    debug(numbers)
    debug("----------")
    largest = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                debug("{} + {}".format(numbers[i], numbers[j]))
                ni = copy.deepcopy(numbers[i])
                nj = copy.deepcopy(numbers[j])
                mag = (ni + nj).magnitude()
                if mag > largest:
                    largest = mag
            else:
                debug("LOL")
    return largest

answerAndSubmit(day, solveA, solveB, 4140, 3993)
