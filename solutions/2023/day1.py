from aoc_util import *

import regex as re

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  1       >24h              0       >24h              0
"""

day = 1

def solveA(lines):
    acc = 0
    for l in lines:
        # v1 = re.match(r"^[A-z\s]*(\d)", l)
        # v2 = re.match(r"(\d)[A-z]*\r", l)   <- not sure why this doesn't work
        dig1 = None
        dig2 = None
        for c in l:
            if c.isdigit():
                dig2 = c
                if dig1 == None:
                    dig1 = c
        if dig1 == None:
            continue
        acc += int(dig1 + dig2)
    return acc

def wordToInt(w):
    if w.isdigit():
        return int(w)
    wordDict = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    return wordDict[w]

def solveB(lines):
    acc = 0
    for l in lines:
        grps = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", l, overlapped=True)
        print(grps)
        acc += wordToInt(grps[0]) * 10 + wordToInt(grps[-1])

    return acc

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 209, 281)
