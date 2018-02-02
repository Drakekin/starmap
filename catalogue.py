import json
import math
import csv
import random
from collections import defaultdict


def invert(l):
    o = [list() for _ in range(len(max(l, key=len)))]
    for i in l:
        for n, v in enumerate(i):
            o[n].append(v)
    return o


with open("starcatalogue.json") as json_catalogue:
    RAW_STARMAP = json.load(json_catalogue)["Stars"]


with open("starnames.csv") as csv_names:
    STARNAMES = [name.lower() for name, mag, ra, dec in csv.reader(csv_names)]
    STARNAME_MARKOV = defaultdict(lambda: [])
    for name in STARNAMES:
        for n, char in enumerate(name):
            STARNAME_MARKOV[name[max(0, n-3):n]].append(char)
        STARNAME_MARKOV[name[-3:]].append(None)


def get_star_name():
    name = ""
    while True:
        char = random.choice(STARNAME_MARKOV[name[max(0, len(name) - 3):]])
        if char is None:
            if len(name) < 3:
                continue
            return name
        name += char


class Star:
    def __init__(self, HDC, HIP, rectascension, declination, distance,
                 brightness, color):
        self.hdc = HDC
        self.hip = HIP
        # self.name = get_star_name(rectascension, declination)
        self.rect_ascension = rectascension
        self.declination = declination
        self.distance = distance
        self.brightness = brightness
        self.color = color

    @property
    def position(self):
        x = math.sin(self.rect_ascension / 180 * math.pi) * math.cos(
            self.declination / 180 * math.pi) * self.distance
        y = math.sin(self.rect_ascension / 180 * math.pi) * math.sin(
            self.declination / 180 * math.pi) * self.distance
        z = math.cos(self.rect_ascension / 180 * math.pi) * self.distance

        return x, y, z


STARMAP = [Star(0, 0, 0, 0, 0, 0, 0)]

for star in RAW_STARMAP:
    s = Star(**star)
    STARMAP.append(s)
