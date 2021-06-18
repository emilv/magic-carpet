import random
from collections import defaultdict

import colorio
from PIL import Image
from colorio.cs import CIELAB, SrgbLinear
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976, delta_e_cie1994, delta_e_cie2000
from inky.inky_uc8159 import Inky
import numpy


from utils import SATURATION, chunks, log

def color_fit(inky: Inky, image: Image) -> float:
    inky_palette = inky._palette_blend(SATURATION, dtype="uint8")
    palette = [_lab_color(color) for color in chunks(inky_palette[:-3], 3)]

    log("Create histogram")
    histogram = color_histogram(image)

    log("Calculate color errors")
    sample_count = sum(histogram.values())
    errors = numpy.empty(shape=sample_count, dtype=float)
    i = 0
    for color, count in histogram.items():
        error = color_score(color, palette)
        for _ in range(count):
            errors[i] = error
            i += 1

    # Mean squared error
    log("Calculate mean squared error")
    mse = numpy.square(errors).mean()
    log("Found fit!")
    return mse

def _lab_color(color):
    #r, g, b = color
    # rgb = sRGBColor(r, g, b, is_upscaled=True)
    # lab = convert_color(rgb, LabColor)
    lab = CIELAB().from_rgb255(color)
    return lab

def color_score(rgb, palette):
    a = _lab_color(rgb)
    best_diff = float("inf")
    for b in palette:
        #diff = delta_e_cie2000(a, b)
        #diff = delta_e_cie1976(a, b)
        #diff = delta_e_cie1994(a, b)
        diff = colorio.diff.ciede2000(a, b)
        #diff = colorio.diff.cie94(a, b)
        best_diff = min(diff, best_diff)

    return best_diff


def color_histogram(image: Image):
    def _fuzzy(value, upper):
        return random.randint(
            max(value - STEP + 1, 0), min(value + STEP - 1, upper - 1)
        )

    STEP = 24
    result = defaultdict(int)
    for x in range(0, image.width, STEP):
        for y in range(0, image.height, STEP):
            color = image.getpixel((_fuzzy(x, image.width), _fuzzy(y, image.height)))
            result[color] += 1
    return result


if __name__ == "__main__":
    from utils import get_image

    for i in range(3):
        image = get_image()
        image.show(title=f"Image {i}")
        result = color_fit(Inky(), image)
        print(f"Image {i}: {result}")
