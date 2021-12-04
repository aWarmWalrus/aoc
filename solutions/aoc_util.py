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
    data = aocd.get_data(day=dayNumber, year=2021, block=True).splitlines()
    return [int(n) if asInts else n for n in data]

# Returns test input as an array of ints.
def getTestInput(dayNumber, asInts = False):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        return [int(n) if asInts else n.strip() for n in f.readlines()]
