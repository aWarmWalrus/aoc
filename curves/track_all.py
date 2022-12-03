import requests
import numpy as np
import time
import sys
from threading import Timer
from html.parser import HTMLParser
from stats_parser import AOCStats

URL = "https://adventofcode.com/{year}/stats"

def writeStats():
    seconds = time.localtime().tm_sec % 60
    if time.localtime().tm_sec % 60 != 0:
        timeLeft = str(60-seconds).ljust(2)
        print("Time until next read: {}".format(timeLeft), end='\r')
        return
    print("Getting stats: ", time.ctime())

    url = URL.format(year = "2022")
    response = requests.get(url)

    parser = AOCStats()
    parser.feed(response.text)
    with open("data/aocstats.csv", "a") as f:
        line = str(time.ctime()) + ","
        for k, v in sorted(parser.getData().items()):
            line += "{},{}".format(v["both"].rjust(7), v["firstOnly"].rjust(7))
            if (k.strip() == "25"):
                line += "\n"
            else:
                line += ","
        print(line)
        f.write(line)

maxIters = 86400
iters = 0
def writeStatsLoop():
    global iters
    iters += 1
    if iters >= maxIters:
        return
    writeStats()

    t = Timer(1.0, writeStatsLoop)
    t.start()

writeStatsLoop()
