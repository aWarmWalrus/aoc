from aoc_util import *

import regex

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
        digits = [int(x) for x in regex.findall(r'(\d)', l)]
        if len(digits) == 0:
            continue
        acc += digits[0] * 10 + digits[-1]
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
        grps = regex.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", l, overlapped=True)
        acc += wordToInt(grps[0]) * 10 + wordToInt(grps[-1])

    return acc

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 209, 281)
