import aocd

def debug(msg):
    print(" > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer):
    actualAns = ansFn(testInput)
    print("============================================")
    print("> [Check tests] Expected: {}  Actual: {}".format(testAnswer, actualAns))
    if (testAnswer == actualAns):
        print("> [Test passed] Answer: {}".format(ansFn(actualInput)))
    else:
        print("> [Test failed]")

# Returns test input as an array of ints.
def getInput(dayNumber):
    return [int(n) for n in aocd.get_data(day=dayNumber).splitlines()]

# Returns test input as an array of ints.
def getTestInput(dayNumber):
    testFileName = "test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        test_lines = list(map(int, f.readlines()))
    return test_lines
