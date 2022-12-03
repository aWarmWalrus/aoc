import requests
import numpy as np
import time
from threading import Timer
from html.parser import HTMLParser

class AOCStats(HTMLParser):
    def __init__(self):
        super().__init__()
        self.indents = 0
        self.preIndents = 0
        self.inMain = False
        self.inStats = False
        self.needDay = True
        self.needBoth = True
        self.needFirstOnly = True
        self.allDays = {}
        self.day = ""
        self.both = ""
        self.firstOnly = ""

    def handle_starttag(self, tag, attrs):
        self.indents += 1
        if tag == "main":
            self.inMain = True
        if tag == "pre":
            self.inStats = True
            self.preIndents = self.indents

    def handle_endtag(self, tag):
        self.indents -= 1
        if tag == "main":
            self.inMain = False
        if tag == "pre":
            self.inStats = False
        if self.indents == self.preIndents and self.inStats:
            self.allDays[self.day] = {"both": self.both, "firstOnly": self.firstOnly}
            self.needDay = True
            self.needBoth = True
            self.needFirstOnly = True

    def handle_data(self, data):
        if self.inStats and self.needDay and (self.indents == self.preIndents + 1):
            self.day = int(data)
            self.needDay = False
        elif self.inStats and self.needBoth and (self.indents == self.preIndents + 2):
            self.both = data
            self.needBoth = False
        elif self.inStats and self.needFirstOnly and (self.indents == self.preIndents + 2):
            self.firstOnly= data
            self.needFirstOnly = False

    def getData(self):
        return self.allDays
