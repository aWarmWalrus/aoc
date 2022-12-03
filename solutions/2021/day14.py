from aoc_util import *
from collections import defaultdict
from collections import Counter
from functools import partial

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

    return template, pairs, elements, rules

"""
Optimal approach: Keep a map counting the frequency of pairs.
"""
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

"""
Alternative approach: using generators to lazily evaluate the full sequence.
Each step has its own generator and uses a constant amount of space: just a
single tuple |pair|.

baseGenerator represents the base case, simply iterating over the template
string, while the stepGenerators recursively call their child generators and
perform look ups into the rules to generate their own next char.
"""
def baseGenerator(template):
    for c in template:
        yield c

def stepGenerator(base, rules):
    pair = (None, None)
    for c in base:
        pair = (pair[1], c)
        if pair[0] is not None:
            yield pair[0]
            if "".join(pair) in rules.keys():
                yield rules["".join(pair)]
    yield pair[1]

def applyGenerator(template, rules, numSteps):
    gen = baseGenerator(template)
    for i in range(numSteps):
        gen = stepGenerator(gen, rules)

    accum = ""
    elements = Counter()
    for c in gen:
        elements[c] += 1
        accum += c
    return max(elements.values()) - min(elements.values())

def solveA(lines, optimal=False):
    if optimal:
        # Do it the boring way.
        # mem usage and time are both O(n), where n is num steps.
        _, pairs, elements, rules = parseLines(lines)
        return apply(pairs, rules, elements, 10)
    else:
        # Do it the cool way: lazily evaluated generators.
        # mem usage is O(n), and time is O(2^n), where n is num steps.
        template, _, _, rules = parseLines(lines)
        return applyGenerator(template, rules, 10)

def solveB(lines):
    _, pairs, elements, rules = parseLines(lines)
    return apply(pairs, rules, elements, 40)

answerAndSubmit(day, solveA, solveB, 1588, 2188189693529)
