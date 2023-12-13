from aoc_util import *
from aoc_algos import *

import numpy as np
import regex
from collections import deque, defaultdict, Counter
import math
import functools

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 12

def parseInput(lines):
    springs = []
    for l in lines:
        lft = l.split()[0]
        rgt = [int(i) for i in l.split()[1].split(',')]
        springs.append((lft, rgt))
    return springs


def fits(row, ints):
    cnts = []
    for g in row.split('.'):
        if g == '':
            continue
        cnts.append(len(g))
    if len(cnts) != len(ints):
        return False
    for c in range(len(cnts)):
        if cnts[c] != ints[c]:
            return False
    return True


def couldFit(row, ints):
    groups = []
    partialKnownGroups = 0
    for g in row.split('.'):
        if g == '':
            continue
        if '#' in g:
            partialKnownGroups += 1
        groups.append(g)
    # If there are already too many groups, then its gg.
    if partialKnownGroups > len(ints):
        return False
    for c in range(min(len(groups), len(ints))):
        # if the group is shorter than required, doesn't even matter.
        if '#' in groups[c] and len(groups[c]) < ints[c]:
            # print("pruned: ", groups, ints)
            return False
        if '?' in groups[c]:
            # The group isn't fully known yet so we have to give it a chance.
            return True
        if len(groups[c]) != ints[c]:
            # print("Doesn't fit! ", row, cnts, ints)
            return False
    return True


@functools.cache
def arrangements(map, counts):
    if '?' not in map:
        return 1 if fits(map, counts) else 0
    sum = 0
    if not couldFit(map, counts):
        return 0
    for c in range(len(map)):
        if map[c] != "?":
            continue
        dmgd = map[:c] + '#' + map[c+1:]
        fixd = map[:c] + '.' + map[c+1:]
        sum += arrangements(dmgd, counts)
        sum += arrangements(fixd, counts)
        break
    return sum


def allPossibilitiesForCount(group, count):
    if '?' not in group:
        return [group]
    groups = list(filter(lambda x: x != '', group.split('.')))
    if len(groups) > 1:
        return []
    print(groups)
    for g in groups:
        if '?' not in g and len(g) > count:
            return []

    for c in range(len(group)):
        if group[c] == '?':
            dmgd = group[:c] + '#' + group[c+1:]
            fixd = group[:c] + '.' + group[c+1:]
            return allPossibilitiesForCount(fixd, count) + allPossibilitiesForCount(dmgd, count)
    exit("literally not possible")


def waysToFit(count, group):
    print(allPossibilitiesForCount(group, count))
        # if

memo = {}

def alt(map, counts):
    if (map, tuple(counts)) in memo:
        return memo[(map, tuple(counts))]

    if len(counts) == 0:
        return 1 if "#" not in map else 0

    count = counts[0]
    total = 0
    for c in range(len(map)):
        if c + count > len(map):
            break
        hasDots = "." in map[c:c+count]
        if (not hasDots and (c+count==len(map) or map[c+count] != '#')):
            total += alt(map[c+count+1:], counts[1:])
        if map[c] == '#':
            break
    memo[(map, tuple(counts))] = total
    return total


@functools.cache
def backtrack(map, counts, depth):
    print("{}{}  {}".format(" |"*depth, map, counts))
    if len(counts) == 0:
        return 0 if '#' in map else 1

    total = 0
    count = counts[0]
    for c in range(len(map)):
        if '.' in map[c:c+count]:
            break
        total += backtrack(map[c+count+1:], counts[1:], depth+1)

    return total




def solveA(lines):
    springs = parseInput(lines)
    tot = 0
    for s in springs:
        print(s)
        p = arrangements(s[0],tuple(s[1]))
        # p = alt(s[0], s[1])
        # p = backtrack(s[0], tuple(s[1]), 0)
        print(p)
        tot += p
    return tot
    # return sum([arrangements(s, 0) for s in springs])


def solveB(lines):
    springs = parseInput(lines)
    unfolded = []
    for s in springs:
        ns = ("?".join([s[0]]*5), s[1]*5)
        unfolded.append(ns)
    all = 0
    for s in unfolded:
        print(s)
        p = alt(s[0], s[1])
        print(p)
        all += p
    return all
    # return sum([arrangements(s, 0) for s in unfolded])


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 21, 525152)
