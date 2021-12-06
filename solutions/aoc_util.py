import aocd

def debug(msg):
    print("\033[1;32;40m > {}".format(msg))

def answer(ansFn, actualInput, testInput, testAnswer, doActual = False):
    actualAns = ansFn(testInput)
    print("\033[1;37;40m============================================")
    print("\033[1;37;40m> [Check tests] Expected: {}  Actual: {}".format(testAnswer, actualAns))
    if (testAnswer == actualAns) and doActual:
        print("\033[1;37;40m>\033[0;37;40m \033[1;32;40m[Test passed] \033[0;32;40mAnswer: {}".format(ansFn(actualInput)))
    else:
        print("\033[1;37;40m>\033[0;37;40m \033[1;31;40m[Test failed]")

# Returns test input as an array of ints.
def getInput(dayNumber, asInts = False):
    data = aocd.get_data(day=dayNumber, year=2021, block=True).splitlines()
    return [int(n) if asInts else n for n in data]

# Returns test input as an array of ints.
def getTestInput(dayNumber, asInts = False):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        return [int(n) if asInts else n.strip() for n in f.readlines()]
