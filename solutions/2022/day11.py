from aoc_util import *

import regex
from collections import defaultdict, deque
from math import prod

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 11

class Monkey:
    def __init__(self, id):
        self._id = id

    def __str__(self):
        return "Monkey {}: items{}\n  op({})\n  test(divis by {})\n  if true({}) else ({})".format( \
            self._id, self._items, self._opStr, self._t, self._ifSucceed, self._ifFail)

    def getID(self):
        return self._id

    def setItems(self, items):
        self._items = items

    def setOperation(self, op, opStr):
        self._op = op
        self._opStr = opStr

    def setTest(self, t):
        self._t = t

    def getTest(self):
        return self._t

    def setIfSucceed(self, succeed):
        self._ifSucceed = int(succeed)

    def setIfFail(self, fail):
        self._ifFail = int(fail)

    def addItem(self, item):
        self._items.append(item)

    def popItem(self):
        if len(self._items) == 0:
            return None
        return self._items.pop(0)

    def causeWorry(self, initial):
        # print(self._opStr, " where old = ", initial)
        op, val = regex.findall(r'old (\S) (\S+)', self._opStr)[0]
        if val == "old":
            return initial * initial
        elif op == "*":
            return initial * int(val)
        elif op == "+":
            return initial + int(val)
        return None

    def getNextMonkey(self, worry):
        if worry % self._t == 0:
            return self._ifSucceed
        else:
            return self._ifFail


def parseMonkeys(lines):
    curr = None
    monkeys = defaultdict()
    for l in lines:
        if regex.search(r'Monkey', l) is not None:
            monkeyID = regex.findall(r'Monkey (\d):', l)[0]
            curr = Monkey(int(monkeyID))
        elif regex.search(r'Starting items', l) is not None:
            items = regex.findall(r'(\d+)', l)
            curr.setItems([int(i) for i in items])
        elif regex.search(r'Operation', l) is not None:
            op, val = regex.findall(r'new = old (\S) (\S+)', l)[0]
            opStr = "old {} {}".format(op, val)
            if val == "old":
                curr.setOperation(lambda x: x * x, "old * old")
            elif op == "*":
                curr.setOperation(lambda x: x * int(val), "old * " + val)
            elif op == "+":
                curr.setOperation(lambda x: x + int(val), "old + " + val)
        elif regex.search(r'Test', l) is not None:
            divisBy = regex.findall(r'(\d+)', l)[0]
            curr.setTest(int(divisBy))
        elif regex.search(r'If true', l) is not None:
            monkey = regex.findall(r'(\d+)', l)[0]
            curr.setIfSucceed(int(monkey))
        elif regex.search(r'If false', l) is not None:
            monkey = regex.findall(r'(\d+)', l)[0]
            curr.setIfFail(int(monkey))
        else:
            monkeys[curr.getID()] = curr

    monkeys[curr.getID()] = curr
    return monkeys


def solveA(lines):
    monkeyDict = parseMonkeys(lines)
    monkeyQueue = []
    monkeyCounter = defaultdict(int)
    for m in sorted(monkeyDict.values(), key=lambda m:m.getID()):
        monkeyQueue.append(m)

    rounds = 0
    while rounds < 20:
        for m in monkeyQueue:
            nextItem = m.popItem()
            while nextItem is not None:
                monkeyCounter[m.getID()] += 1
                worry = m.causeWorry(nextItem)
                worry = int(worry / 3)
                monkeyDict[m.getNextMonkey(worry)].addItem(worry)

                nextItem = m.popItem()
        rounds += 1

    return prod(sorted(monkeyCounter.values(), reverse=True)[0:2])

def solveB(lines):
    monkeyDict = parseMonkeys(lines)
    monkeyQueue = []
    monkeyCounter = defaultdict(int)
    maxWorry = 1
    for m in sorted(monkeyDict.values(), key=lambda m:m.getID()):
        monkeyQueue.append(m)
        maxWorry *= m.getTest()

    rounds = 0
    while rounds < 10000:
        for m in monkeyQueue:
            nextItem = m.popItem()
            while nextItem is not None:
                monkeyCounter[m.getID()] += 1
                worry = m.causeWorry(nextItem) % maxWorry
                monkeyDict[m.getNextMonkey(worry)].addItem(worry)

                nextItem = m.popItem()
        rounds += 1

    return prod(sorted(monkeyCounter.values(), reverse=True)[0:2])

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 10605, 2713310158)
