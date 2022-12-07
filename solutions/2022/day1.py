from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  1       >24h  160923      0       >24h  154818      0
"""

day = 1

def solveA(lines):
    mostCals = 0
    currentCals = 0
    for l in lines:
        if len(l) == 0:
            if currentCals > mostCals:
                mostCals = currentCals
            currentCals = 0
            continue
        currentCals += int(l)

    return mostCals

def solveB(lines):
    cals = []
    currentCals = 0
    for l in lines:
        if len(l) == 0:
            cals += [currentCals]
            currentCals = 0
            continue
        currentCals += int(l)
    cals += [currentCals]
    cals = sorted(cals)

    return sum(cals[-3:])

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 24000, 45000)
