from bitstring import BitArray
from aoc_util import *

"""
[Day 16 Results]
  Part 1
    > time: 00:48:44
    > rank: 1225
  Part 2
    > time: 01:00:09
    > rank: 1068
"""

day = 16

def doOperation(typeId, literals):
    if typeId == 0:
        return sum(literals)
    elif typeId == 1:
        result = 1
        for i in literals:
            result *= i
        return result
    elif typeId == 2:
        return min(literals)
    elif typeId == 3:
        return max(literals)
    elif typeId == 5:
        return 1 if literals[0] > literals[1] else 0
    elif typeId == 6:
        return 1 if literals[0] < literals[1] else 0
    elif typeId == 7:
        return 1 if literals[0] == literals[1] else 0
    raise Error("Invalid type: " + str(type))


def parseLiteralPacket(bin):
    version = int(bin[0:3], 2)
    typeId = int(bin[3:6], 2)
    iter = 6
    nums = ''
    oneMore = True
    while oneMore:
        if bin[iter] == '0':
            oneMore = False
        nums += bin[iter+1:iter+5]
        iter += 5
    return version, iter, int(nums, 2)


def parseOperatorPacket(bin):
    version = int(bin[0:3], 2)
    typeId = int(bin[3:6], 2)
    assert(typeId != 4)

    versions = version
    literals = []
    iter = 0

    lengthTypeId = int(bin[6])
    if lengthTypeId == 0:
        totalLength = int(bin[7:22], 2)
        lengthTraveled = 0
        iter = 22
        while (lengthTraveled < totalLength):
            v, length, ans = parsePacket(bin[iter:])
            versions += v
            lengthTraveled += length
            iter += length
            literals.append(ans)
    else:
        totalSubs = int(bin[7:18], 2)
        subpacketsProcessed = 0
        iter = 18
        while (subpacketsProcessed < totalSubs):
            v, length, ans = parsePacket(bin[iter:])
            versions += v
            subpacketsProcessed += 1
            iter += length
            literals.append(ans)

    return versions, iter, doOperation(typeId, literals)


def parsePacket(bin):
    typeId = int(bin[3:6], 2)
    if typeId == 4:
        return parseLiteralPacket(bin)
    else:
        return parseOperatorPacket(bin)


def solveA(lines, optimal=False):
    c = BitArray(hex=lines[0])
    vs, _, _ = parsePacket(c.bin)
    return vs


def solveB(lines, optimize=True):
    c = BitArray(hex=lines[0])
    _, _, ans = parsePacket(c.bin)
    return ans


answerAndSubmit(day, solveA, solveB, 20, 1)
