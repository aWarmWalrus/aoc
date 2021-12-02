import aocd

def debug(msg):
    print(" > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer, doActual = False):
    actualAns = ansFn(testInput)
    print("============================================")
    print("> [Check tests] Expected: {}  Actual: {}".format(testAnswer, actualAns))
    if (testAnswer == actualAns) and doActual:
        print("> [Test passed] Answer: {}".format(ansFn(actualInput)))
    else:
        print("> [Test failed]")

# Returns test input as an array of ints.
def getInput(dayNumber, asInts = False):
    if asInts:
        return [int(n) for n in aocd.get_data(day=dayNumber).splitlines()]
    return [n for n in aocd.get_data(day=dayNumber).splitlines()]

# Returns test input as an array of ints.
def getTestInput(dayNumber, asInts = False):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        if asInts:
            return list(map(int, f.readlines()))
        return [l.strip() for l in f.readlines()]

def getTestInputAsText(dayNumber):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        test_lines = f.readlines()
    return test_lines
