from aoc_util import *

import time
import sys
import os
import numpy as np
from collections import deque
from heapq import *

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 13

def parseHelper(subs):
    if subs == "":
        return []
    acc = []
    i = -1
    intAcc = ""
    while i < len(subs) - 1:
        i += 1
        if subs[i].isnumeric():
            intAcc += subs[i]
            continue
        if intAcc != "":
            acc.append(int(intAcc))
            intAcc = ""

        if subs[i] == ',':
            continue
        if subs[i] == '[':
            closer = i
            levels = 1
            for c in range(i + 1, len(subs)):
                if subs[c] == '[':
                    levels += 1
                elif subs[c] == ']':
                    levels -= 1
                    if levels == 0:
                        closer = c

            acc.append(parseHelper(subs[i+1:closer]))
            i = closer + 1
            continue
        if subs[i] == ']':
            exit("this should never happen")
        exit("this too should never happen")
    if intAcc != "":
        acc.append(int(intAcc))
    return acc

# def parseHelper(subs):
#     print("parseHelper({})".format(subs))
#     acc = []
#     skipTo = 0
#     for c in range(len(subs)):
#         if skipTo > c:
#             continue
#         if subs[c].isnumeric():
#             if c+1 < len(subs) and subs[c+1].isnumeric():
#                 acc.append(int(subs[c:c+2]))
#                 skipTo = c+2
#             else:
#                 acc.append(int(subs[c]))
#         elif subs[c] == ',':
#             continue
#         elif subs[c] == '[':
#             if subs[c+1] == ']':
#                 acc.append([])
#                 skipTo = c + 2
#             closer = c
#             levels = 0
#             for i in range(c, len(subs)):
#                 if subs[i] == '[':
#                     levels += 1
#                 elif subs[i] == ']':
#                     levels -= 1
#                     if levels == 0:
#                         closer = i
#             if closer == c:
#                 exit("NOOOOOOOOOOOO")
#
#             acc.append(parseHelper(subs[c+1:closer]))
#             skipTo = closer + 1
#         elif subs[c] == ']':
#             return acc
#         else:
#             panic("unexpected input: ", subs[c])
#     return acc


def parseList(lin):
    print("parseList({})".format(lin))
    return parseHelper(lin[1:-1])


def solveA(lines):

    def compare(v1, v2):
        if isinstance(v1, list) and isinstance(v2, list):
            for i in range(len(v1)):
                if i >= len(v2):
                    # print("v2 is shorter")
                    return False
                if not compare(v1[i], v2[i]):
                    # print("v1[i] {}   > v2[i] {}".format(v1[i], v2[i]))
                    return False
            return True
        elif isinstance(v1, list) and isinstance(v2, int):
            return compare(v1, [v2])
        elif isinstance(v1, int) and isinstance(v2, list):
            return compare([v1], v2)
        elif isinstance(v1, int) and isinstance(v2, int):
            return v1 <= v2
        else:
            exit("HUHHHHHHHHHHHHHHHHHHH???")

    def goodPair(p1, p2, i):
        pack1 = parseList(p1)
        pack2 = parseList(p2)
        res = compare(pack1, pack2)
        if res:
            print(i / 3 + 1, pack1, pack2, end="\n\n")
            return int(i / 3) + 1
        return 0

    return sum([goodPair(lines[i], lines[i+1], i) for i in range(0,len(lines),3)])

def solveB(lines):
    return 0

if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 13, 1)
