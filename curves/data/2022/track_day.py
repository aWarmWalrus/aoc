"""
2022 version of track_day. This year, I don't want to have to start this
script every freaking day. It will just track the current day's stats, for 24
hours until the next day starts.

Run instructions:
  python track_day.py <year>
"""
import requests
import numpy as np
import os.path
import pytz
import sys
import time
from stats_parser import AOCStats
from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
from threading import Timer
from html.parser import HTMLParser

YEAR = 2022
URL  = "https://adventofcode.com/{year}/stats"
FILE = "C:/Users/awarm/Documents/GitHub/aoc/curves/data/{}/day{}.csv"

def minutesSinceRelease():
    now = datetime.now(pytz.timezone("EST"))
    midnight = now.replace(day=now.day, hour=0, minute=0, second=0, microsecond=0)
    return int((now - midnight).total_seconds() / 60)

def getStats(day):
    url = URL.format(year = YEAR)
    response = requests.get(url)

    parser = AOCStats()
    parser.feed(response.text)
    return parser.getData()


def writeStats(day, data):
    filename = FILE.format(YEAR, day)
    if not os.path.exists(filename):
        # Write the header
        with open(filename, "a") as f:
            f.write("minutes,both,half\n")

    with open(filename, "a") as f:
        line = "{},{},{}\n".format(minutesSinceRelease(), data[day]["both"], data[day]["firstOnly"])
        print("Getting stats (Day {})  \n   {}".format(day, line))
        f.write(line)

def writeStatsLoop():
    t = Timer(0.98, writeStatsLoop)
    t.start()

    now = datetime.now(pytz.timezone("EST"))

    interval = 60  # wait one minute between each read
    if now.second % interval != 0:
        timeLeft = str(interval - (now.second % interval))
        print("Time until next read: {:2}".format(timeLeft), end='\r')
        return

    writeStats(now.day, getStats(now.day))

writeStatsLoop()
