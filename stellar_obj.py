import math
import random

from stellar_data import STAR_CLASS, SPECIAL_NAMES
from util import distance


class Star:
    def __init__(self, HDC, HIP, rectascension, declination, distance,
                 brightness, color, name=None):
        if name is None:
            name = self.special_names(HIP)
        self.hdc = HDC
        self.hip = HIP
        self.name = name if name else "HIP " + str(HIP)
        self.rect_ascension = rectascension
        self.declination = declination
        self.distance = distance
        self._stellar_class = STAR_CLASS.get(str(self.hip), "G5")

        self._planets = []
        self._closest_stars = None

    @property
    def stellar_class(self):
        if len(self._stellar_class) < 2:
            return "G", 2
        letter, number = self._stellar_class[:2]
        letter = letter.upper()
        if letter not in "OBAFGKM":
            return "G", 2
        if number not in "0123456789":
            number = 5
        else:
            number = int(number)

        return letter, number

    @property
    def temperature(self):
        temps = {
            "O": (30000, 10000),
            "B": (10000, 30000),
            "A": (7500, 10000),
            "F": (6000, 7500),
            "G": (5200, 6000),
            "K": (3700, 5200),
            "M": (2400, 3700),
        }

        letter, number = self.stellar_class
        min_t, max_t = temps[letter]
        mod = number / 9
        return min_t + (max_t - min_t) * mod

    @property
    def mass(self):
        masses = {
            "O": (16, 120),
            "B": (2.1, 16),
            "A": (1.4, 2.1),
            "F": (1.04, 1.4),
            "G": (0.8, 1.04),
            "K": (0.45, 0.8),
            "M": (0.08, 0.45),
        }

        letter, number = self.stellar_class
        min_t, max_t = masses[letter]
        mod = number / 9
        return min_t + (max_t - min_t) * mod

    @property
    def radius(self):
        radius = {
            "O": (6.6, 50),
            "B": (1.8, 6.6),
            "A": (1.4, 1.8),
            "F": (1.15, 1.4),
            "G": (0.96, 1.15),
            "K": (0.7, 0.96),
            "M": (0.1, 0.7),
        }

        letter, number = self.stellar_class
        min_t, max_t = radius[letter]
        mod = number / 9
        return min_t + (max_t - min_t) * mod

    @property
    def luminosity(self):
        luminosity = {
            "O": (30000, 100000),
            "B": (25, 30000),
            "A": (5, 25),
            "F": (1.5, 5),
            "G": (0.6, 1.5),
            "K": (0.08, 0.6),
            "M": (0, 0.08),
        }

        letter, number = self.stellar_class
        min_t, max_t = luminosity[letter]
        mod = number / 9
        return min_t + (max_t - min_t) * mod

    @property
    def habitable_zone(self):
        return math.sqrt(self.luminosity / 1.1), math.sqrt(self.luminosity / 0.53)

    @property
    def frost_line(self):
        min_hab, max_hab = self.habitable_zone
        return max_hab * 2.25

    def _generate_planets(self):
        planets = []

        num_planets = random.randint(5, 12)
        inners = num_planets // 2
        outers = num_planets - inners

        frost_line = self.frost_line * 215
        inner_swathe = (frost_line - 50) / inners
        outer_swathe = (4100 - frost_line) / outers

        for n in range(num_planets):
            if n < inners:
                orbital_radius = (inner_swathe * random.random() + (inner_swathe * n) + 50) / 215
            else:
                orbital_radius = (outer_swathe * random.random() + (outer_swathe * n) + frost_line + 50) / 215
            planets.append(Planet(self, orbital_radius))

        return planets

    @property
    def planets(self):
        if not self._planets:
            self._planets = self._generate_planets()

        return self._planets

    def closest_stars(self, starmap):
        if self._closest_stars is None:
            self._closest_stars = list(
                sorted([(s, distance(self.position, s.position)) for s in starmap], key=lambda p: p[1]))[1:]
        return self._closest_stars

    @property
    def position(self):
        x = math.sin(self.rect_ascension / 180 * math.pi) * math.cos(
            self.declination / 180 * math.pi) * self.distance
        y = math.sin(self.rect_ascension / 180 * math.pi) * math.sin(
            self.declination / 180 * math.pi) * self.distance
        z = math.cos(self.rect_ascension / 180 * math.pi) * self.distance

        return x, y, z

    def __hash__(self):
        return self.hip

    def __repr__(self):
        return "<Star ({})>".format(self.name)

    def special_names(self, HIP):
        return SPECIAL_NAMES.get(HIP)


class Planet:
    def __init__(self, star, orbital_distance, population=0, name=None, founding_year=None):
        self.orbital_distance = orbital_distance
        self.founding_year = founding_year
        self.rocky = self.orbital_distance < star.frost_line
        self._name = name
        self.population = population
        self.star = star

    @property
    def habitable(self):
        min_hab, max_hab = self.star.habitable_zone
        return min_hab <= self.orbital_distance <= max_hab

    @property
    def orbital_period(self):
        au_in_m = 1.496e+11
        orbit_m = self.orbital_distance * au_in_m
        orbit_m_3 = orbit_m ** 3
        stellar_kg = 1.988e30
        star_kg = self.star.mass * stellar_kg
        newtons_grav_constant = 6.67408e-11
        mu = star_kg * newtons_grav_constant
        return 2 * math.pi * math.sqrt(orbit_m_3 / mu) / 86400

    @property
    def name(self):
        if self._name:
            return self._name
        return self.star.name + " " + "abcdefghijklmn"[self.star.planets.index(self)]

    def growth_rate(self, current_year):
        if self.founding_year is None:
            return 1
        effective_year = current_year - self.founding_year
        predicted = 1.009725 + \
                    0.001393539 * effective_year - \
                    0.00005792155 * (effective_year ** 2) + \
                    8.629435e-7 * (effective_year ** 3) - \
                    4.54325e-9 * (effective_year ** 4)
        return max(1.005, predicted)

    def grow(self, current_year):
        if self.founding_year is None:
            return
        self.population = int(self.population * self.growth_rate(current_year))