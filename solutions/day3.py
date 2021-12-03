from aoc_util import *

day = 3

def solveA(lines):
    g = ""
    e = ""
    numBits = len(lines[0])
    for n in range(numBits):
        ones = 0
        zeroes = 0
        for line in lines:
            if line[n] == "1":
                ones += 1
            elif line[n] == "0":
                zeroes += 1
        if ones > zeroes:
            g += "1"
            e += "0"
        else:
            g += "0"
            e += "1"

    return int(g, 2) * int(e, 2)

def solveB(lines):
    def getRating(lines, isFlipped):
        bits = ""
        for n in range(len(lines[0])):
            ones = 0
            zero = 0
            for line in lines:
                if line[n] == "1":
                    ones += 1
                elif line[n] == "0":
                    zero += 1
            if ones >= zero:
                bits += "0" if isFlipped else "1"
            elif zero > ones:
                bits += "1" if isFlipped else "0"
            else:
                raise Error('wtf')
            filtered = []
            for line in lines:
                if line.startswith(bits):
                    filtered.append(line)
            if (len(filtered) == 1):
                return int(filtered[0], 2)
            lines = filtered
        return 0
    return getRating(lines, False) * getRating(lines, True)

answer(solveA, getInput(day), getTestInput(day), 198, True)
answer(solveB, getInput(day), getTestInput(day), 230, True)
