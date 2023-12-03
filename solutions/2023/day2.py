from aoc_util import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  2       >24h              0       >24h              0
"""

day = 2

def isPullValid(pull):
    for k in pull.split(','):
        amt, color = k.split()
        if color == "red":
            if int(amt) > 12:
                return False
        elif color == "green":
            if int(amt) > 13:
                return False
        elif color == "blue":
            if int(amt) > 14:
                return False
    return True

    
def solveA(lines):
    validIDs = 0
    for l in lines:
        gameID, pulls = l.split(':')
        if all([isPullValid(p) for p in pulls.split(';')]):
            gID = int(gameID.split()[1])
            validIDs += gID
    return validIDs


def maxColors(game):
    reds = 0
    greens = 0
    blues = 0
    for pull in game.split(';'):
        for k in pull.split(','):
            amt, color = k.split()
            if color == "red" and int(amt) > reds:
                reds = int(amt)
            elif color == "green" and int(amt) > greens:
                greens = int(amt)
            elif color == "blue" and int(amt) > blues:
                blues = int(amt)
    return reds, greens, blues


def solveB(lines):
    sum = 0
    for l in lines:
        gameID, pulls = l.split(':')
        reds, greens, blues = maxColors(pulls)
        sum += reds * greens * blues
    return sum


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 8, 2286)
