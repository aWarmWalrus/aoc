from aoc_util import *

from collections import defaultdict

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  5   00:20:56    3016      0   00:23:03    2516      0
"""

day = 5

def parseCrates(lines):
    stacks = defaultdict(list)
    for s in lines:
        i = 1
        for pos in range(1,len(s),4):
            if s[pos].isalpha():
                stacks[i] = [s[pos]] + stacks[i]
            i += 1
    return stacks

def solveA(lines):
    cratesIndex = 0
    for l in lines:
        if len(l) > 1 and l[1] == "1":
            break
        cratesIndex += 1
    stacks = parseCrates(lines[:cratesIndex])
    for l in lines[cratesIndex+2:]:
        m, num, f, fromNum, t, toNum = l.split(' ')
        amt = int(num)
        src = int(fromNum)
        dst = int(toNum)

        for i in range(amt):
            stacks[dst].append(stacks[src].pop())
    tops = ""
    for _, stack in sorted(stacks.items()):
        tops += stack.pop()
    return tops

def solveB(lines):
    cratesIndex = 0
    for l in lines:
        if len(l) > 1 and l[1] == "1":
            break
        cratesIndex += 1
    stacks = parseCrates(lines[:cratesIndex])
    for l in lines[cratesIndex+2:]:
        m, num, f, fromNum, t, toNum = l.split(' ')
        amt = int(num)
        src = int(fromNum)
        dst = int(toNum)

        tmpStack = []
        for i in range(amt):
            tmpStack.append(stacks[src].pop())
        for _ in range(amt):
            stacks[dst].append(tmpStack.pop())
    tops = ""
    for _, stack in sorted(stacks.items()):
        tops += stack.pop()
    return tops

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, "CMZ", "MCD", strip=False)
