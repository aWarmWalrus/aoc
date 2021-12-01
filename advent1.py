import aocd
from aocd import numbers

day_number = 1

# Leave this code in for convenience and consistency.
def debug(msg):
    print(" > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer):
    print("============================================")
    print("Puzzle Answer: {}".format(ansFn(actualInput)))
    print("Expected Test Answer: {}".format(testAnswer))
    print("Our Test Answer: {}".format(ansFn(testInput)))

# Start coding here.
def advent1a(lines):
    ups = 0
    for i in range(1, len(lines)):
        if (lines[i] > lines[i-1]):
            ups = ups + 1
    return ups

def advent1b(lines):
    windowSize = 3
    ups = 0
    for i in range(windowSize + 1, len(lines)+1):
        j = i - 1
        windowA = sum(lines[j-windowSize:j])
        windowB = sum(lines[i-windowSize:i])
        if (windowB > windowA):
            ups = ups + 1
    return ups

# Boilerplate code
testFileName = "day_{}_test.txt".format(day_number)
with open(testFileName) as f:
    test_lines = list(map(int, f.readlines()))

# Boilerplate get code.
lines = [int(n) for n in aocd.get_data(day=day_number).splitlines()]

answer(advent1a, lines, test_lines, 7)
answer(advent1b, lines, test_lines, 5)
