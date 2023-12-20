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
        ruleHead, ruleTail = None, None
        for cat, compare, val, succ in mainRules:
            rule = Rule(cat, compare, val, succ)
            if ruleHead is None:
                ruleHead = rule
            if ruleTail is not None:
                ruleTail.fail = rule
            ruleTail = rule
        name, lastFail = regex.findall(r'(\w+)(?:{|})', line)
        ruleHead.name = name
        ruleTail.fail = lastFail
        workflows[name] = ruleHead
    return workflows, parts


def solveA(lines):
    workflows, parts = parseInput(lines)
    total = 0
    for p in parts:
        curr = workflows["in"]
        while True:
            pVal = p[curr.category]
            passes = (pVal > curr.val) if curr.compare == ">" else (pVal < curr.val)
            next = curr.success if passes else curr.fail
            if next == "A":
                total += sum(p.values())
                break
            elif next == "R":
                break
            elif isinstance(next, str):
                curr = workflows[next]
            elif isinstance(next, Rule):
                curr = next
            else:
                exit("unexpected case")
    return total


def rangeOverlap(r1, r2):
    if r1[0] > r2[0]:    # Set r1 to be the smaller range.
        r1, r2 = r2, r1
    if r1[1] < r2[0]:    # No overlap
        return None
    return (r2[0], min(r1[1], r2[1]))


def subtractRange(toSub, series):
    newS = []
    for seg in series:
        olap = rangeOverlap(toSub, seg)
        if olap is None:       # No overlap
            newS.append(seg)
            continue
        elif olap == seg:      # toSub totally surrounds segment
            continue
        if seg[0] < olap[0]:   # Capture left part of segment (if any)
            newS.append((seg[0], olap[0]))
        if seg[1] > olap[1]:   # Capture right part of segment (if any)
            newS.append((olap[1], seg[1]))
    return newS


def collapseRange(ranges):
    acc = {}
    for key, series in ranges.items():
        acc[key] = sum([s[1] - s[0] for s in series])
    return acc


def acceptableParts(workflows, rule, ranges):
    if rule == "A":
        return math.prod(collapseRange(ranges).values())
    if rule == "R":
        return 0

    if isinstance(rule, str):
        rule = workflows[rule]

    # Relevant range when condition is met
    posRange = (rule.val+1, 4001) if rule.compare == ">" else (1, rule.val)
    # Relevant range when condition is not met
    negRange = (1, rule.val+1) if rule.compare == ">" else (rule.val, 4001)

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
