from aoc_util import *

"""
[Day 2 Results]
  Part 1
    > time: 00:08:37
    > rank: 6051
  Part 2
    > time: 00:12:31
    > rank: 5456
"""

day = 2

def solveA(lines):
    x = 0
    y = 0
    for line in lines:
        dir, amtStr = line.split(' ')
        amt = int(amtStr)
        if (dir == "forward"):
            x += amt
        elif (dir == "down"):
            y += amt
        elif (dir == "up"):
            y -= amt
    return x * y

def solveB(lines):
    x = 0
    y = 0
    aim = 0
    for line in lines:
        dir, amtStr = line.split(' ')
        amt = int(amtStr)
        if (dir == "forward"):
            x += amt
            y += aim * amt
        elif (dir == "down"):
            aim += amt
        elif (dir == "up"):
            aim -= amt
    return x * y

answer(solveA, getInput(day), getTestInput(day), 150, True)
answer(solveB, getInput(day), getTestInput(day), 900, True)
