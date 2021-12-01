from aoc_util import *

day_number = 1

def solveA(lines):
    ups = 0
    for i in range(1, len(lines)):
        if (lines[i] > lines[i-1]):
            ups = ups + 1
    return ups

def solveB(lines):
    windowSize = 3
    ups = 0
    for i in range(windowSize + 1, len(lines)+1):
        j = i - 1
        windowA = sum(lines[j-windowSize:j])
        windowB = sum(lines[i-windowSize:i])
        if (windowB > windowA):
            ups = ups + 1
    return ups

answer(solveA, getInput(day_number), getTestInput(day_number), 7)
answer(solveB, getInput(day_number), getTestInput(day_number), 5)
