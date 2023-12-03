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
    strength, cycle, addx = 0, 0, 0
    register = 1
    while len(lines) > 0 or addx != 0:
        cycle += 1
        if (cycle - 20) % 40 == 0:
            strength += register * cycle
        if addx != 0:
            register += addx
            addx = 0
            continue
        inst = lines.pop(0)
        if inst.startswith("addx"):
            addx = int(inst.split()[1])
    return strength

def solveB(lines):
    cycle, addx = 0, 0
    spr = 1
    while len(lines) > 0 or addx != 0:
        cycle += 1
        pos = cycle % 40
        print("##" if pos <= spr + 2 and pos >= spr else "  ", \
            end="" if cycle % 40 != 0 else "\n")
        if addx != 0:
            spr += addx
            addx = 0
            continue
        inst = lines.pop(0)
        if inst.startswith("addx"):
            addx = int(inst.split()[1])
    return "EHBZLRJR"

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 13140, "EHBZLRJR")
