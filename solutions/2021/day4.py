from aoc_util import *

"""
[Day 4 Results]
  Part 1
    > time: 00:39:23
    > rank: 3803
  Part 2
    > time: 00:41:07
    > rank: 2657
"""

day = 4

class BingoBoard:
    def __init__(self, lines):
        self.rows = []
        self.hits = []
        for line in lines:
            self.rows.append([int(n) for n in line.split()])
            self.hits.append([0 for i in range(5)])
        self.movesRequired = 0
        self.sumRemaining = sum([sum(row) for row in self.rows])

    def processInput(self, input):
        for x in range(5):
            for y in range(5):
                if input == self.rows[x][y]:
                    self.hits[x][y] = 1
                    self.sumRemaining -= input
                    # To make sure it doesn't hit again for some reason.
                    self.rows[x][y] = -1
        self.movesRequired += 1

    def isWin(self):
        for row in self.hits:
            if sum(row) == 5:
                return True
        for col in range(5):
            columns = [self.hits[n][col] for n in range(5)]
            if sum(columns) == 5:
                return True

    def boardValue(self, lastInput):
        return self.sumRemaining * lastInput

    def processAll(self, inputs):
        for input in inputs:
            self.processInput(input)
            if self.isWin():
                return self.movesRequired, self.boardValue(input)


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

answerAndSubmit(day, solveA, solveB, 4512, 1924)
