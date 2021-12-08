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

def debugDict(dic):
    debug("{")
    for k, v in sorted(dic.items()):
        debug("  {} -> {}".format(k, v))
    debug("}")

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

Frequency of each segment across all the digits
a = 8 (solved by diffing 7 (acf) and 1 (cf))
b = 6 (unique)
c = 8 (unique, aside from a)
d = 7
e = 4 (unique)
f = 9 (unique)
g = 7
"""
def decodeWord(word, decoder):
    lengthToNumber = {2: "1", 3: "7", 4: "4", 7: "8"}
    if len(word) in lengthToNumber.keys():
        return lengthToNumber[len(word)]

    display = ""
    for c in word:
        display += decoder[c]
    corrected = "".join(sorted(display))

    two = "acdeg"
    three = "acdfg"
    five = "abdfg"
    six = "abdefg"
    nine = "abcdfg"
    zero = "abcefg"
    displayToNumber = {two: "2", three: "3", five: "5", six: "6", nine: "9", zero: "0"}

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

        # Get the signals that have unique occurrence frequencys. These would be
        # |b, c, e, and f| which occur 6, 8, 4, and 9 times respectively.
        # 'a' also occurs 8 times, but we just solved that.
        frequencies = Counter("".join(preamble))
        for signal, count in sorted(frequencies.items()):
            if (count == 6):
                decoder[signal] = "b"
            elif (count == 4):
                decoder[signal] = "e"
            elif (count == 8) and decoder[signal] == "":
                decoder[signal] = "c"
            elif (count == 9):
                decoder[signal] = "f"

        # Get 'd' by finding the segment of 4 that hasn't been decoded yet.
        # In other words, 4 is made of four segments: |b c d f|. We just solved
        # |b c f| above. So the last signal in our scrambled 4 that isn't solved
        # yet must map to 4's last segment, 'd'.
        for c in scrambled[4]:
            if c not in decoder.keys():
                decoder[c] = "d"
                break

        # Finally, 'g' is the last segment that we need to solve. By process of
        # elimination, the one letter that isn't in our decoder must map to 'g'.
        for i in "abcdefg":
            if i not in decoder.keys():
                decoder[i] = "g"
                break

        # Decode.
        total += int("".join([decodeWord(word, decoder) for word in output]))

    return total

answerAndSubmit(day, solveA, solveB, 26, 61229)
