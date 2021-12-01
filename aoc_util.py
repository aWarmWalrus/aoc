import aocd

def debug(msg):
    print(" > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer):
    print("============================================")
    print("Puzzle Answer: {}".format(ansFn(actualInput)))
    print("Expected Test Answer: {}".format(testAnswer))
    print("Our Test Answer: {}".format(ansFn(testInput)))

# Returns test input as an array of ints.
def getInput(dayNumber):
    return [int(n) for n in aocd.get_data(day=dayNumber).splitlines()]

# Returns test input as an array of ints.
def getTestInput(dayNumber):
    testFileName = "day_{}_test.txt".format(dayNumber)
    with open(testFileName) as f:
        test_lines = list(map(int, f.readlines()))
    return test_lines
