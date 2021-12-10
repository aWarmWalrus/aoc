"""
Run instructions:
  python track_day.py <day>
"""
import requests
import numpy as np
import time
import pytz
import sys
from stats_parser import AOCStats
from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
from threading import Timer
from html.parser import HTMLParser

URL = "https://adventofcode.com/{year}/stats"

def secondsSinceRelease(day):
    now = datetime.now(pytz.timezone("EST"))
    midnight = now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)
    return int((now - midnight).total_seconds())

def icon(va):
    if va % 4 == 0:
        return "|"
    elif va % 4 == 1:
        return "/"
    elif va % 4 == 2:
        return "-"
    elif va % 4 == 3:
        return "\\"

def writeStats(day):
    seconds = secondsSinceRelease(day)
    if seconds < 0:
        countdown = timedelta(seconds = (seconds * -1))
        print("Problem not released yet. ({}) {} remaining.".format(icon(seconds), countdown), end='\r')
        return

    interval = 60  # time between reads
    if seconds % interval != 0:
        timeLeft = str(interval - (seconds % interval))
        print("Time until next read: {}".format(timeLeft), end='\r')
        return

    url = URL.format(year = "2021")
    response = requests.get(url)

    parser = AOCStats()
    parser.feed(response.text)
    filename = "data/day{}.csv".format(day)
    with open(filename, "a") as f:
        data = parser.getData()
        line = "{},{},{}\n".format(int(seconds / 60), data[day]["both"], data[day]["firstOnly"])
        print("Getting stats (Day {})  \n   {}".format(day, line))
        f.write(line)

if len(sys.argv) < 2:
    print("Please specify a day: python track_day.py <day>")
    exit()

maxIters = 86400
day = int(sys.argv[1])
iters = 0
def writeStatsLoop():
    global iters
    iters += 1
    if iters >= maxIters:
        return
    writeStats(day)

    t = Timer(0.95, writeStatsLoop)
    t.start()

writeStatsLoop()
