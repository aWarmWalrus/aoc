import aocd
import logging

PRINT_DEBUG = True
YEAR = 2023

def color(txt, color):
    if color == "green":
        c = 32
    elif color == "white":
        c = 37
    elif color == "red":
        c = 31
    return "\033[1;{};40m{}\033[0;37;40m".format(c, txt)

def debug(msg, end="\n"):
    if PRINT_DEBUG:
        print(color(" > {}".format(msg), "white"), end=end)

def checkAndSubmit(day, ansFn, expectedOut, part, stripWhitespace):
    testInput = getTestInput(day, stripWhitespace)
    if (type(expectedOut) == list):
        print(color("[Check tests] Multiple test cases", "white"))
        if len(expectedOut) == 0:
            print(color("  No test cases provided", "red"))
            return False
        if len(expectedOut) != len(testInput):
            print(color("  {} tests provided does not match {} expectations provided"\
                .format(len(testInput), len(expectedOut)), "red"))
            return False

        numFailed = 0
        for i in range(len(testInput)):
            testOut = ansFn(testInput[i].strip())
            print(color("  Test {}:  Expected: {}  Actual: {}"\
                    .format(i, expectedOut[i], testOut), "white" if expectedOut[i] == testOut else "red"))
            if expectedOut[i] != testOut:
                numFailed += 1
        if numFailed > 0:
            print(color("[Tests failed]: {} cases failed".format(numFailed), "red"))
            return False

        print(color("[Tests passed] :)", "green"))
        return True

    testOut = ansFn(testInput)
    fullInput = getInput(day)
    print(color("[Check tests]  Expected: {}  Actual: {}"\
            .format(expectedOut, testOut), "white"))

    if (expectedOut == testOut):
        answer = ansFn(fullInput)
        print(color("[Test passed] ", "green") + \
            color("Answer: {}".format(answer), "white"))
        print(color("[Submitting] ", "white"), end="")
        aocd.submit(answer, part, day=day, year=YEAR)
        return True
    else:
        print(color("[Test failed] ", "red"))
        return False


def answerAndSubmit(day, ansFnA, ansFnB, expectedOutputA, expectedOutputB=None, strip=True):
    print(color("Part A ======================================", "white"))
    if not checkAndSubmit(day, ansFnA, expectedOutputA, "a", strip):
        return

    if expectedOutputB == None:
        return

    print(color("Part B ======================================", "white"))
    checkAndSubmit(day, ansFnB, expectedOutputB, "b", strip)


# Returns test input as an array of strings.
def getInput(day):
    return aocd.get_data(day=day, year=YEAR, block=True).splitlines()

# Returns test input as an array of strings.
def getTestInput(dayNumber, stripWhitespace):
    testFileName = "tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        return [l.strip() if stripWhitespace else l for l in f.readlines()]
