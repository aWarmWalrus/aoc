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

def answer(ansFn, actualInput, testInput, testAnswer, doActual = False):
    actualAns = ansFn(testInput)
    print(color("============================================", "white"))
    print(color("> [Check tests] Expected: {}  Actual: {}"\
            .format(testAnswer, actualAns), "white"))
    if (testAnswer == actualAns) and doActual:
        print(color("> ", "white") + \
            color("[Test passed] ", "green") + \
            color("Answer: {}".format(ansFn(actualInput)), "white"))
    else:
        print(color("> ", "white") + \
            color("[Test failed] ", "red"))

# Returns test input as an array of ints.
def getInput(dayNumber, asInts = False):
    data = aocd.get_data(day=dayNumber, year=2021, block=True).splitlines()
    return [int(n) if asInts else n for n in data]

# Returns test input as an array of ints.
def getTestInput(dayNumber, asInts = False):
    testFileName = "../tests/test{}.txt".format(dayNumber)
    with open(testFileName) as f:
        return [int(n) if asInts else n.strip() for n in f.readlines()]
