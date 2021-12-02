from aoc_util import *

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
            y += amt
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
            aim += amt
    return x * y

answer(solveA, getInput(day), getTestInput(day), 150, True)
answer(solveB, getInput(day), getTestInput(day), 900, True)
