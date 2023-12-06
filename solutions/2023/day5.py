from aoc_util import *

import numpy as np
import regex
from collections import defaultdict
from math import inf

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  5   00:29:32    2952      0   02:58:33    6506      0
"""

day = 5

def parseInput(lines):
    seeds = [int(i) for i in lines[0].split()[1:]]
    allMaps = []
    # Maps will be lists of tuples.
    currMap = []
    for line in lines[2:]:
        if len(line) == 0:
            continue
        if line[0].isalpha():
            if len(currMap) == 0:
                continue
            allMaps.append(sorted(currMap))
            currMap = []
            continue
        dst, src, l = [int(i) for i in line.split()]
        currMap.append((src, dst, l))
    allMaps.append(sorted(currMap))
    return seeds, allMaps


def solveA(lines):
    seeds, maps = parseInput(lines)
    lowestVal = inf
    for s in seeds:
        curr = s
        for map in maps:
            for (src, dst, l) in map:
                if curr >= src and curr < src + l:
                    curr = dst + curr - src
                    break
        if curr < lowestVal:
            lowestVal = curr
    return lowestVal

    
# start is inclusive, end is not inclusive
def mapSeedRange(start, end, mapIndex, maps):
    if mapIndex >= len(maps):
        return start, end - start
    lowestVal = inf
    lastTop = 0
    totalSeeds = 0
    for (rBottom, rTarget, rL) in maps[mapIndex]:
        rTop = rBottom + rL
        if rTop <= start:
            # The range doesn't overlap with the seeds at all.
            lastTop = rTop
            continue
        if rBottom > end:
            # No ranges starting from this one will overlap with the seed range.
            break

        # Handle the portion of the seed range that doesn't overlap with any
        # mapping range.
        if lastTop >= start and rBottom > start and rBottom != lastTop:
            res, seeds = mapSeedRange(lastTop, rBottom, mapIndex+1, maps)
            if res < lowestVal:
                lowestVal = res
            totalSeeds += seeds
        elif lastTop < start and rBottom > start and rBottom != lastTop:
            res, seeds = mapSeedRange(start, rBottom, mapIndex+1, maps)
            if res < lowestVal:
                lowestVal = res
            totalSeeds += seeds

        newStart = start
        newEnd = end
        if rBottom <= start and rTop >= end:
            # 1. The mapping range fully encapsulates the seed range.
            delta = start - rBottom
            newStart = rTarget + delta
            newEnd = rTarget + (end - start) + delta
        elif rBottom <= start and (rTop > start and rTop < end):
            # 2. The mapping range overlaps with the bottom of seed range.
            delta = start - rBottom
            newStart = rTarget + delta
            newEnd = rTarget + (rTop - start) + delta
        elif (rBottom > start and rBottom < end) and rTop >= end:
            # 3. The mapping range overlaps with the top of the seed range.
            newStart = rTarget
            newEnd = rTarget + (end - rBottom)
        elif rBottom > start and rTop < end:
            # 4. The mapping range is encapsulated BY the seed range.
            newStart = rTarget
            newEnd = rTarget + (rTop - rBottom)

        res, seeds = mapSeedRange(newStart, newEnd, mapIndex+1, maps)
        if res < lowestVal:
            lowestVal = res
        lastTop = rTop
        totalSeeds += seeds

    if lastTop < start:
        # 5. All of the mapping ranges are lower than the beginning of the seed range.
        res, seeds = mapSeedRange(start, end, mapIndex+1, maps)
        if res < lowestVal:
            lowestVal = res
        totalSeeds += seeds
    elif lastTop < end:
        # 6. All of the mapping ranges are lower than the end of the seed range.
        res, seeds = mapSeedRange(lastTop, end, mapIndex+1, maps)
        if res < lowestVal:
            lowestVal = res
        totalSeeds += seeds
    return lowestVal, totalSeeds


def solveB(lines):
    seeds, maps = parseInput(lines)
    lowestVal = inf
    for s in range(0, len(seeds), 2):
        firstSeed = seeds[s]
        numSeeds = seeds[s+1]
        val, endSeeds = mapSeedRange(firstSeed, firstSeed+numSeeds, 0, maps)
        if val < lowestVal:
            lowestVal = val
    return lowestVal


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 35, 46)
