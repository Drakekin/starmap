import json
import random

from stellar_data import STARMAP, get_star_name
from util import filter_by_distance

print("There are {} stars".format(len(STARMAP)))

CURRENT_YEAR = 130

for _ in range(170):
    print("IT IS ", CURRENT_YEAR + 1950)
    for star in STARMAP:
        for planet in star.planets:
            planet.grow(CURRENT_YEAR)
            # if planet.population > 0:
                # print(planet.name, "has a population of", "{:,}".format(planet.population), "and is growing by",
                #       str(round((planet.growth_rate(CURRENT_YEAR) - 1) * 100, 2)) + "%")
            if planet.population > 1e8:
                colonists = int(planet.population * 0.05)
                planet.population -= colonists

                colonisation_candidates = [s for s in filter_by_distance(20, planet.star.closest_stars(STARMAP)) if any(p.habitable for p in s.planets)]
                while colonists > 0:
                    destination_star = random.choice(colonisation_candidates)
                    destination_planet = random.choice([p for p in destination_star.planets if p.habitable])
                    if destination_planet.founding_year is None:
                        destination_planet.founding_year = CURRENT_YEAR
                        if str(destination_star.hip) in destination_star.name:
                            destination_star.name = get_star_name()
                            print("HIP", destination_star.hip, "was renamed", destination_star.name, "when it was colonised!")
                        print(destination_planet.name, "was colonised!")
                    destination_planet.population += min(1e6, colonists)
                    colonists -= min(1e6, colonists)

    CURRENT_YEAR += 1

output = [star.to_json() for star in STARMAP]
with open("colony_map.json", "w") as out_file:
    json.dump(output, out_file)

print()
