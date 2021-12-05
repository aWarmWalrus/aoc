from aoc_util import *
import numpy as np

"""
[Day 4 Re-do]

Retrying Day 4, except using numpy to perform some of the elementary linalg.
"""

day = 4

class BingoBoard:
    def __init__(self, lines):
        self.rows = np.empty((5,5), dtype=int)
        for i in range(len(lines)):
            self.rows[i] = np.array([int(n) for n in lines[i].split()])
        self.hits = np.zeros((5,5),dtype=int)
        self.moves = 0
        self.sumRemaining = np.sum(self.rows)

    def processInput(self, input):
        if (input in self.rows):
            row, col = np.where(self.rows == input)
            self.hits[row,col] = 1
            self.rows[row,col] = -1
            self.sumRemaining -= input
        self.moves += 1

    def isWin(self):
        rowWin = np.sum(self.hits,axis=0)
        colWin = np.sum(self.hits,axis=1)
        if 5 in np.concatenate([rowWin, colWin]):
            return True

    def processAll(self, inputs):
        for input in inputs:
            self.processInput(input)
            if self.isWin():
                return self.moves, self.sumRemaining * input

def solveA(lines):
    input = [int(n) for n in lines[0].split(',')]
    fewest = 100000
    winningBoard = 0
    for i in range(2, len(lines), 6):
        b = BingoBoard(lines[i:i+5])
        moves, boardValue = b.processAll(input)
        if moves < fewest:
            winningBoard = boardValue
            fewest = moves
    return winningBoard

def solveB(lines):
    input = [int(n) for n in lines[0].split(',')]
    most = 0
    winningBoard = 0
    for i in range(2, len(lines), 6):
        b = BingoBoard(lines[i:i+5])
        moves, boardValue = b.processAll(input)
        if moves > most:
            winningBoard = boardValue
            most = moves
    return winningBoard

answer(solveA, getInput(day), getTestInput(day), 4512, True)
answer(solveB, getInput(day), getTestInput(day), 1924, True)
