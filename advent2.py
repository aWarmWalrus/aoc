import aocd
from aocd import numbers

day_number = 2

# Leave this code in for convenience and consistency.
def debug(msg):
    print(" > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer):
    print("============================================")
    print("Puzzle Answer: {}".format(ansFn(actualInput)))
    print("Expected Test Answer: {}".format(testAnswer))
    print("Our Test Answer: {}".format(ansFn(testInput)))

# Start coding here.
def solveA(lines):
    return 0

def solveB(lines):
    return 0

# Boilerplate code
testFileName = "day_{}_test.txt".format(day_number)
with open(testFileName) as f:
    test_lines = list(map(int, f.readlines()))

# Boilerplate get code.
lines = [int(n) for n in aocd.get_data(day=day_number).splitlines()]

answer(solveA, lines, test_lines, 0)
answer(solveB, lines, test_lines, 0)
