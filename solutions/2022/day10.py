from aoc_util import *

import numpy as np

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 10   00:24:32    5171      0   00:36:17    3181      0
"""

day = 10

def solveA(lines):
    strength = 0
    cycle = 0
    toAdd = 0
    register = 1
    while len(lines) > 0 or toAdd != 0:
        cycle += 1
        if (cycle - 20) % 40 == 0:
            strength += register * cycle
        if toAdd != 0:
            register += toAdd
            toAdd = 0
            continue
        inst = lines.pop(0)
        if inst == "noop":
            continue
        elif inst.startswith("addx"):
            toAdd = int(inst.split()[1])
        else:
            panic("hmm")
    return strength

def solveB(lines):
    cycle = 0
    toAdd = 0
    register = 1
    while len(lines) > 0 or toAdd != 0:
        cycle += 1
        pos = cycle % 40
        if pos <= register + 2 and pos >= register:
            print("#", end="")
        else:
            print(" ", end="")
        if (cycle % 40) == 0:
            print()

        if toAdd != 0:
            register += toAdd
            toAdd = 0
            continue
        inst = lines.pop(0)
        if inst == "noop":
            continue
        # inst.startswith("addx"):
        toAdd = int(inst.split()[1])
    return "EHBZLRJR"

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 13140, "EHBZLRJR")
