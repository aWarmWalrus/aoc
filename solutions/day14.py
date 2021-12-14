from aoc_util import *
from collections import defaultdict

"""
[Day 14 Results]
  Part 1
    > time: 00:28:19
    > rank: 4951
  Part 2
    > time: 00:28:46
    > rank: 871
"""

day = 14

def parseLines(lines):
    template = lines[0]
    rules = defaultdict(str)
    for i in range(2, len(lines)):
        pair, ins = lines[i].split(' -> ')
        rules[pair] = ins

    pairs = defaultdict(int)
    elements = defaultdict(int)
    for p in range(len(template) - 1):
        pairs[template[p:p+2]] += 1
        elements[template[p]] += 1
    elements[template[-1]] += 1

    return pairs, elements, rules

def apply(pairs, rules, elements, numSteps):
    for i in range(numSteps):
        newPairs = defaultdict(int)
        for pair, count in pairs.items():
            if pair in rules.keys():
                ins = rules[pair]
                newPairs[pair[0] + ins] += count
                newPairs[ins + pair[1]] += count
                elements[ins] += count
            else:
                newPairs[pair] = pairs[pair]
        pairs = newPairs
    return max(elements.values()) - min(elements.values())

def solveA(lines):
    pairs, elements, rules = parseLines(lines)
    return apply(pairs, rules, elements, 10)

def solveB(lines):
    pairs, elements, rules = parseLines(lines)
    return apply(pairs, rules, elements, 40)

answerAndSubmit(day, solveA, solveB, 1588, 2188189693529)
