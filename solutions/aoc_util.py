import aocd

def color(txt, color):
    if color == "green":
        c = 32
    elif color == "white":
        c = 37
    elif color == "red":
        c = 31
    return "\033[1;{};40m{}\033[0;37;40m".format(c, txt)

def debug(msg):
    print("\033[1;32;40m > {}".format(msg))

def checkAndSubmit(day, ansFn, expectedOut, part):
    testInput = getTestInput(day)
    testOut = ansFn(testInput)
    fullInput = getInput(day)
    print(color("> [Check tests] Expected: {}  Actual: {}"\
            .format(expectedOut, testOut), "white"))
    if (expectedOut == testOut):
        answer = ansFn(fullInput)
        print(color("> ", "white") + \
            color("[Test passed] ", "green") + \
            color("Answer: {}".format(answer), "white"))
        print(color("> [Submitting] ", "white"), end="")
        aocd.submit(answer, part, day=day, year=2021)
        return True
    else:
        print(color("> ", "white") + \
            color("[Test failed] ", "red"))
        return False


def answerAndSubmit(day, ansFnA, ansFnB, expectedOutputA, expectedOutputB=None):
    print(color("> Part A ======================================", "white"))
    if not checkAndSubmit(day, ansFnA, expectedOutputA, "a"):
        return

    if expectedOutputB == None:
        return

    print(color("> Part B ======================================", "white"))
    checkAndSubmit(day, ansFnB, expectedOutputB, "b")


# Returns test input as an array of ints.
def getInput(dayNumber):
    return aocd.get_data(day=dayNumber, year=2021, block=True).splitlines()

# Returns test input as an array of ints.
def getTestInput(dayNumber):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        return [n.strip() for n in f.readlines()]
