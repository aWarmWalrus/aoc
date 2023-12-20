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
        self.compare = comp
        self.val = int(val)
        self.success = success
        self.fail = None

    def setName(self, name):
        self.name = name

    def setFail(self, fail):
        self.fail = fail

    def performTest(self, part):
        catVal = part[self.category]
        passes = (catVal > self.val) if self.compare == ">" else (catVal < self.val)
        return self.success if passes else self.fail

    def __str__(self):
        acc = ""
        if len(self.name) > 0:
            acc += self.name + "{"
        acc += self.category + self.compare + str(self.val) + ":" + self.success + ","
        if isinstance(self.fail, Rule):
            acc += str(self.fail)
        else:
            acc += self.fail + "}"
        return acc

    def __repr__(self):
        return str(self)


def parseInput(lines):
    workflows = {}
    parts = []
    for line in lines:
        if line == "":
            continue
        elif line[0] == "{":
            expr = r'(\w)=(\d+)'
            part = {}
            matches = regex.findall(expr, line)
            for l, v in matches:
                part[l] = int(v)
            parts.append(part)
            continue
        mainRules = regex.findall(r'(\w)(<|>)(\d+):(\w+)', line)
        ruleHead = None
        rule = None
        for cat, compare, val, succ in mainRules:
            nr = Rule(cat, compare, val, succ)
            if rule is not None:
                rule.setFail(nr)
            else:
                ruleHead = nr
            rule = nr
        name, lastFail = regex.findall(r'(\w+)(?:{|})', line)
        ruleHead.setName(name)
        rule.setFail(lastFail)
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
                total += sum(p.values())
                break
            elif res == "R":
                break
            elif isinstance(res, str):
                curr = workflows[res]
            elif isinstance(res, Rule):
                curr = res
            else:
                exit("unexpected case")
    return total


def rangeOverlap(r1, r2):
    # Set r1 to be the smaller range.
    if r1[0] > r2[0]:
        r1, r2 = r2, r1
    # No overlap
    if r1[1] < r2[0]:
        return None
    return (r2[0], min(r1[1], r2[1]))


def subtractRange(toSub, series):
    # subtract range into series (i.e. adding a new REJECT range)
    newS = []
    for seg in series:
        olap = rangeOverlap(toSub, seg)
        # No overlap
        if olap is None:
            newS.append(seg)
            continue
        # toSub totally surrounds segment
        elif olap == seg:
            # Just don't add it to newS
            continue
        # Capture part of segment left of the overlap (if any)
        if seg[0] < olap[0]:
            nRL = (seg[0], olap[0])
            newS.append(nRL)
        # Capture part of segment right of the overlap (if any)
        if seg[1] > olap[1]:
            nRR = (olap[1], seg[1])
            newS.append(nRR)
    return newS


def collapseRange(ranges):
    acc = {}
    for key, series in ranges.items():
        acc[key] = sum([s[1] - s[0] for s in series])
    return acc


def acceptableParts(workflows, rule, ranges):
    # Base case
    if rule == "A":
        return math.prod(collapseRange(ranges).values())
    if rule == "R":
        return 0

    if isinstance(rule, str):
        rule = workflows[rule]

    # Relevant range when condition is met, when comparison is >
    posRange = (rule.val+1, 4001)
    # Relevant range when condition is not met, when comparison is >
    negRange = (1, rule.val+1)
    if rule.compare == "<":
        posRange = (1, rule.val)
        negRange = (rule.val, 4001)

    succRanges = ranges.copy()
    succRanges[rule.category] = subtractRange(negRange, ranges[rule.category])

    failRanges = ranges.copy()
    failRanges[rule.category] = subtractRange(posRange, ranges[rule.category])

    return acceptableParts(workflows, rule.success, succRanges) + acceptableParts(workflows, rule.fail, failRanges)


def solveB(lines):
    workflows, _ = parseInput(lines)
    initRanges = {
        'x':[(1,4001)],
        'm':[(1,4001)],
        'a':[(1,4001)],
        's':[(1,4001)],
    }
    return acceptableParts(workflows, workflows["in"], initRanges)


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 19114, 167409079868000)
