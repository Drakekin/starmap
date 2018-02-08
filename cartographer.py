import json
import random

from PIL import Image, ImageDraw, ImageColor

from stellar_obj import Star
from util import filter_to_inhabited

WHITE = (256, 256, 256, 255)
RED = (256,0,0,256)
BLUE = (128,128,256,256)
GREY = (128, 128, 128, 255)
DARK_GREY = (64, 64, 64, 255)
TRANSPARENT_GREY = (64, 64, 64, 128)
BLACK = (0, 0, 0, 255)


def load_galaxy(galaxy_json_path):
    with open(galaxy_json_path) as galaxy_json_file:
        galaxy_json = json.load(galaxy_json_file)
        return [Star(**star) for star in galaxy_json]


def draw_map(starmap, size=1024):
    inhabited_space = filter_to_inhabited(starmap)
    print(len(inhabited_space))
    radius = max(star.distance for star in inhabited_space)
    print(radius)

    map_image = Image.new("RGBA", (size, size), BLACK)
    canvas = ImageDraw.Draw(map_image)

    border = size * .125
    inner = size * .75
    inner_half = inner / 2
    midpoint = size * .5

    canvas.ellipse(((border, border + inner * .25), (border + inner, border + inner * .75)), outline=DARK_GREY)

    for star in inhabited_space:
        wx, wy, wz = star.position
        sx = midpoint + inner_half * (wx / radius)
        plane_sy = midpoint + inner_half * (wy / radius / 2)
        sy = plane_sy + inner_half * (wz / radius)
        star_size = (wy + radius) / (radius * 2) * 3.5 + 0.5
        # canvas.line(((sx, plane_sy), (sx, sy)), DARK_GREY, 1)
        canvas.ellipse(((sx - star_size, sy - star_size), (sx + star_size, sy + star_size)),
                       fill=random.choice([RED,BLUE]) if any(planet.population > 0 for planet in star.planets) else GREY)

    return map_image


if __name__ == '__main__':
    colony_map = load_galaxy("colony_map2.json")
    with open("colony.png", "wb") as output:
        draw_map(colony_map, 2048).save(output, "PNG")
