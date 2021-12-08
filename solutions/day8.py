from aoc_util import *
import numpy as np
from collections import defaultdict
from collections import Counter

"""
[Day 8 Results]
  Part 1
    > time: 00:09:29
    > rank: 1687
  Part 2
    > time: 01:03:07
    > rank: 2281
"""

day = 8

def parseLine(line):
    p, o = line.split(" | ")
    return p.split(" "), o.split(" ")

def solveA(lines):
    total = 0
    for line in lines:
        preamble, output = parseLine(line)
        for word in output:
            if len(word) in [2, 4, 3, 7]:
                total += 1
    return total

"""
Length of word -> which number it could represent
len 2: 1
len 3: 7
len 4: 4
len 5: 2, 3, 5
len 6: 0, 6, 9
len 7: 8

Number of occurrences of a signal for each digit (0-9)
a = solved
b = 6 (solved)
c = 8 (solved)
d = 7
e = 4 (solved)
f = 9 (solved)
g = 7
"""

TWO = "acdeg"
THREE = "acdfg"
FIVE = "abdfg"
SIX = "abdefg"
NINE = "abcdfg"
ZERO = "abcefg"

def debugDict(dic):
    debug("{")
    for k, v in sorted(dic.items()):
        debug("  {} -> {}".format(k, v))
    debug("}")

def decodeWord(word, decoder):
    if len(word) == 2:
        return "1"
    if len(word) == 3:
        return "7"
    if len(word) == 4:
        return "4"
    if len(word) == 7:
        return "8"

    display = ""
    for c in word:
        display += decoder[c]
    corrected = "".join(sorted(display))

    displayToNumber = {TWO: "2", THREE: "3", FIVE: "5", SIX: "6", NINE: "9", ZERO: "0"}

    return displayToNumber[corrected]

def solveB(lines):
    total = 0
    for line in lines:
        preamble, output = parseLine(line)

        # Decoder maps a faulty signal to the segment it represents.
        decoder = defaultdict(str)

        # Get the signal that maps to 'a'
        # i.e. the only segment that is in 7 but not in 1.
        scrambled = ["" for i in range(10)]
        for word in preamble:
            if len(word) == 4:
                scrambled[4] = word
            elif len(word) == 3:
                scrambled[7] = word
            elif len(word) == 2:
                scrambled[1] = word
        for i in scrambled[7]:
            if not i in scrambled[1]:
                decoder[i] = "a"

        # Get the signals that have unique occurrence frequencys.
        # These are |b, c, e, and f| which occur 6, 8, 4, and 9 times
        # respectively across the digits. 'a' also occurs 8 times, but we just
        # solved that.
        frequencies = Counter("".join(preamble))
        for k, count in sorted(frequencies.items()):
            if (count == 6):
                decoder[k] = "b"
            elif (count == 4):
                decoder[k] = "e"
            elif (count == 8) and decoder[k] == "":
                decoder[k] = "c"
            elif (count == 9):
                decoder[k] = "f"

        # Get 'd' by finding the segment of 4 that hasn't been decoded yet.
        # In other words, 4 is made of four segments: |b c d f|. We should have
        # found |b c f| in the step above. So the signal in our scrambled 4 that
        # isn't mapped yet must map to the last segment, 'd'.
        for c in scrambled[4]:
            if c not in decoder.keys():
                decoder[c] = "d"
                break

        # Finally, 'g' is the last segment that we need to map to. By process of
        # elimination, the only letter that isn't mapped yet must map to 'g'.
        for i in "abcdefg":
            if i not in decoder.keys():
                decoder[i] = "g"
                break

        # Decode.
        correctValue = ""
        for word in output:
            correctValue += str(decodeWord(word, decoder))

        total += int(correctValue)

    return total

answerAndSubmit(day, solveA, solveB, 26, 61229)
