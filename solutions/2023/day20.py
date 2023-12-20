from aoc_util import *
from aoc_algos import *

from collections import deque, defaultdict
import numpy as np
import time

"""
Personal Stats:
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
"""

day = 20

class Module:
    def __init__(self, name, dests, type):
        self.name = name
        self.dests = dests
        self.type = type
        self.val = 0
        self.inputs = {}

    def addInput(self, input):
        self.inputs[input] = 0
        return

    def __repr__(self):
        setting = "({})".format(self.val) if self.type == "%" else ""
        base = "({}{}{}->[{}]".format(self.type, self.name, setting, ",".join(self.dests))
        if self.type == "&" and self.inputs is not None:
            base += " i{}".format(self.inputs)
        base += ")"
        return base


def parseInput(lines):
    modules = {}
    for l in lines:
        id, dests = l.split(' -> ')
        name = id[1:]
        type = id[0]
        if id == "broadcaster":
            name = "broadcaster"
            type = ""
        modules[name] = Module(name, dests.split(', '), type)

    for conj in modules.values():
        if conj.type != '&':
            continue
        for inp in modules.values():
            if conj.name in inp.dests:
                conj.addInput(inp.name)

    if False:   # Create a graphviz .dot file.
        with open('day20.dot', 'w') as f:
            f.write('digraph {\n')
            for src, mod in modules.items():
                f.write('  {} -> {{ {} }}\n'.format(src, " ".join(mod.dests)))
            f.write('}')

    return modules


def solveA(lines):
    modules = parseInput(lines)
    lows, highs = 0, 0
    for i in range(1000):
        fifo = deque([('broadcaster', 0, "button")])
        while len(fifo) > 0:
            dest, sig, src = fifo.popleft()
            lows += 1 if sig == 0 else 0
            highs += 1 if sig == 1 else 0
            if dest not in modules:
                continue
            mod = modules[dest]
            nextSig = 0   # If broadcaster, nextSig is 0.
            if mod.type == '%':
                if sig == 1:
                    continue
                mod.val ^= 1
                nextSig = mod.val
            elif mod.type == '&':
                mod.inputs[src] = sig
                nextSig = 0 if all([v == 1 for v in mod.inputs.values()]) else 1
            for d in mod.dests:
                fifo.append((d, nextSig, dest))

    return lows * highs


def solveB(lines):
    modules = parseInput(lines)
    cycles = {}
    if 'zg' not in modules:
        # Bypass the test input, go straight to real input.
        return 0
    i = 0
    while len(cycles) < 4:
        i += 1
        fifo = deque([('broadcaster', 0, "button")])
        while len(fifo) > 0:
            dest, sig, src = fifo.popleft()
            if dest not in modules:
                continue
            mod = modules[dest]
            nextSig = 0
            # Do logic for figuring out whether to send low or high
            if mod.type == '%':
                if sig == 1:
                    continue
                mod.val ^= 1
                nextSig = mod.val
            elif mod.name == "broadcaster":
                nextSig = 0
            elif mod.type == '&':
                mod.inputs[src] = sig
                if mod.name == 'zg' and any([v == 1 for v in mod.inputs.values()]):
                    for k, v in filter(lambda x: x[1] == 1, mod.inputs.items()):
                        cycles[k] = i
                    print(i, cycles)
                nextSig = 0 if all([v == 1 for v in mod.inputs.values()]) else 1
            for d in mod.dests:
                fifo.append((d, nextSig, dest))
    return math.prod(cycles.values())


if __name__ == "__main__":
    answerAndSubmit(day, solveA, solveB, 11687500, 0)
