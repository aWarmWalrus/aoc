from aoc_util import *

day = 2

def solveA(lines):
    x = 0
    y = 0
    for line in lines:
        dir, amtStr = line.split(' ')
        amt = int(amtStr)
        if (dir == "forward"):
            x = x + amt
        elif (dir == "down"):
            y = y + amt
        elif (dir == "up"):
            y = y - amt
    return x * y

def solveB(lines):
    x = 0
    y = 0
    aim = 0
    for line in lines:
        dir, amtStr = line.split(' ')
        amt = int(amtStr)
        if (dir == "forward"):
            x = x + amt
            y = y + (aim * amt)
        elif (dir == "down"):
            aim = aim + amt
        elif (dir == "up"):
            aim = aim - amt
    return y * x

answer(solveA, getInput(day), getTestInput(day), 150, True)
answer(solveB, getInput(day), getTestInput(day), 900, True)
