from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time
import regex

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 19   00:41:13    2756      0       >24h   14733      0
"""

day = 19

class Rule:
    def __init__(self, condCat, comp, val, success):
        self.name = ""
        self.category = condCat
        self.comp = comp
        self.val = int(val)
        self.success = success
        self.failRule = None
        self.failEnd = None

    def setName(self, name):
        self.name = name

    def setFailRule(self, fr):
        self.failRule = fr

    def setFailEnd(self, fe):
        self.failEnd = fe

    def performTest(self, part):
        passes = None
        if self.comp == ">":
            passes = part[self.category] > self.val
        elif self.comp == "<":
            passes = part[self.category] < self.val
        if passes:
            return self.success
        if self.failRule is None:
            return self.failEnd
        return self.failRule


    def __str__(self):
        acc = ""
        if len(self.name) > 0:
            acc += self.name + "{"
        acc += self.category + self.comp + str(self.val) + ":" + self.success + ","
        if self.failRule is not None:
            acc += self.failRule.__str__()
        if self.failEnd is not None:
            acc += self.failEnd + "}"
        return acc

    def __repr__(self):
        return self.__str__()


def parseInput(lines):
    workflows = {}
    parts = []
    isParts = False
    for line in lines:
        if line == "":
            isParts = True
            continue
        if isParts:
            expr = r'(\w)=(\d+)'
            part = {}
            matches = regex.findall(expr, line)
            for l, v in matches:
                part[l] = int(v)
            parts.append(part)
        else:
            expr = r'(\w)(<|>)(\d+):(\w+)'
            matches = regex.findall(expr, line)
            ruleHead = None
            rule = None
            for cat, comp, val, succ in matches:
                nr = Rule(cat, comp, val, succ)
                if rule is not None:
                    rule.setFailRule(nr)
                else:
                    ruleHead = nr
                rule = nr
            name = line.split('{')[0]
            ruleHead.setName(name)

            failEnd = line.split(',')[-1][:-1]
            rule.setFailEnd(failEnd)
            workflows[name] = ruleHead

    return workflows, parts


def solveA(lines):
    workflows, parts = parseInput(lines)

    total = 0
    for p in parts:
        curr = workflows["in"]
        while True:
            res = curr.performTest(p)
            if res == "A":
                total += p['s'] + p['a'] + p['m'] + p['x']
                break
            elif res == "R":
                break
            elif isinstance(res, str):
                curr = workflows[res]
            elif isinstance(res, Rule):
                curr = res
    return total


def rangeOverlap(r1, r2):
    # Ensure r1 is the smaller range.
    if r1[0] > r2[0]:
        t = r1
        r1 = r2
        r2 = t
    # No overlap
    if r1[1] < r2[0]:
        return None
    return (r2[0], min(r1[1], r2[1]))


def subtractRange(toSub, series):
    # subtract range into series (i.e. adding a new REJECT range)
    newS = []
    for s in series:
        o = rangeOverlap(toSub, s)
        # No overlap
        if o is None:
            newS.append(s)
            continue
        # toSub totally surrounds s
        elif o == s:
            # Just don't add it to newS
            continue
        # s totally surrounds subRange
        elif s[0] < o[0] and s[1] > o[1]:
            nR1 = (s[0], o[0])
            nR2 = (o[1], s[1])
            newS += [nR1, nR2]
        # subtract the left side
        elif o[0] == s[0]:
            nR = (o[1], s[1])
            newS.append(nR)
        elif o[1] == s[1]:
            nR = (s[0], o[0])
            newS.append(nR)
    return newS


def countAccepts(ranges):
    acc = {}
    for key, series in ranges.items():
        tot = 0
        for s in series:
            tot += s[1] - s[0]
        acc[key] = tot
    return acc


def acceptableParts(workflows, rule, ranges):
    # Base case
    if rule == "A":
        return math.prod([ v for v in countAccepts(ranges).values()])
    if rule == "R":
        return 0

    if isinstance(rule, str):
        rule = workflows[rule]

    base = (1,4001)
    # Relevant range when condition is met.
    posRange = base
    # Relevant range when condition is not met.
    negRange = base
    if rule.comp == ">":
        posRange = (rule.val+1, base[1])
        negRange = (base[0], rule.val+1)
    elif rule.comp == "<":
        posRange = (base[0], rule.val)
        negRange = (rule.val, base[1])

    succRanges = ranges.copy()
    failRanges = ranges.copy()

    succRanges[rule.category] = subtractRange(negRange, ranges[rule.category])
    failRanges[rule.category] = subtractRange(posRange, ranges[rule.category])

    failNode = rule.failRule if rule.failRule is not None else rule.failEnd
    return acceptableParts(workflows, rule.success, succRanges) + acceptableParts(workflows, failNode, failRanges)


def solveB(lines):
    workflows, _ = parseInput(lines)

    ranges = {
        'x':[(1,4001)],
        'm':[(1,4001)],
        'a':[(1,4001)],
        's':[(1,4001)],
    }
    return acceptableParts(workflows, workflows["in"], ranges)


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 19114, 167409079868000)
