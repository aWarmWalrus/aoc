# Leave this code in for convenience and consistency.
def debug(msg):
    print(" > {}".format(msg))

def answer(ans):
    print("ANS: {}".format(ans))

# Start coding here.
def advent1_a(lines):
    ups = 0
    for i in range(1, len(lines)):
        if (int(lines[i]) > int(lines[i-1])):
            ups = ups + 1
    return ups

def advent1_b(lines):
    windowSize = 3
    ups = 0
    for i in range(windowSize + 1, len(lines)+1):
        j = i - 1
        windowA = sum(list(map(int, lines[j-windowSize:j])))
        windowB = sum(list(map(int, lines[i-windowSize:i])))
        if (windowB > windowA):
            ups = ups + 1
        debug("{} > {}?".format(windowB, windowA))
    return ups

# Boilerplate code
with open('input_day1.txt') as f:
    lines = f.readlines()

test_lines = ["199", "200", "208", "210", "200", "207", "240", "269", "260", "263"]

answer(advent1_a(lines))
answer(advent1_b(lines))
