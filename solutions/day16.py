import math
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


def debugType(typeId):
    return {0: "SUM",
            1: "PROD",
            2: "MIN",
            3: "MAX",
            5: "GREATER THAN",
            6: "LESS THAN",
            7: "EQUALS TO"}[typeId]


def operate(typeId, literals):
    return {0: lambda l : sum(literals),
            1: lambda l : math.prod(literals),
            2: lambda l : min(literals),
            3: lambda l : max(literals),
            5: lambda l : 1 if literals[0] > literals[1] else 0,
            6: lambda l : 1 if literals[0] < literals[1] else 0,
            7: lambda l : 1 if literals[0] == literals[1] else 0}[typeId](literals)


def parseLiteralPacket(bin, level):
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
    debug("{}literal: {}".format("  " * level, int(nums,2)))
    return version, iter, int(nums, 2)


def parseOperatorPacket(bin, level):
    version = int(bin[0:3], 2)
    typeId = int(bin[3:6], 2)
    assert(typeId != 4)
    debug("{}operator packet: {} <".format("  " * level, debugType(typeId)))

    versions = version
    literals = []
    iter = 0

    lengthTypeId = int(bin[6])
    if lengthTypeId == 0:
        totalLength = int(bin[7:22], 2)
        lengthTraveled = 0
        iter = 22
        while (lengthTraveled < totalLength):
            v, length, ans = parsePacket(bin[iter:], level + 1)
            versions += v
            lengthTraveled += length
            iter += length
            literals.append(ans)
    else:
        totalSubs = int(bin[7:18], 2)
        subpacketsProcessed = 0
        iter = 18
        while (subpacketsProcessed < totalSubs):
            v, length, ans = parsePacket(bin[iter:], level + 1)
            versions += v
            subpacketsProcessed += 1
            iter += length
            literals.append(ans)
    result = operate(typeId, literals)
    debug("{}> {} result: {}".format("  " * level, debugType(typeId), result))

    return versions, iter, operate(typeId, literals)


def parsePacket(bin, level=0):
    typeId = int(bin[3:6], 2)
    if typeId == 4:
        return parseLiteralPacket(bin, level)
    else:
        return parseOperatorPacket(bin, level)


def solveA(lines, optimal=False):
    c = BitArray(hex=lines[0])
    vs, _, _ = parsePacket(c.bin)
    return vs


def solveB(lines, optimize=True):
    c = BitArray(hex=lines[0])
    _, _, ans = parsePacket(c.bin)
    return ans


answerAndSubmit(day, solveA, solveB, 20, 1)
