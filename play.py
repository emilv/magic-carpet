import random
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from inky.inky_uc8159 import Inky

import background.unsplash
import elements.carpe_diem
from clear import clear
from utils import dithered, log, WIDTH, HEIGHT, SATURATION

TEXTMARGIN = 8
DEBUG = len(sys.argv) > 1 and sys.argv[1] == "debug"

inky = Inky()

background_image = background.unsplash.get_best_image(inky)
text_image = elements.carpe_diem.get_carpe_diem(WIDTH, HEIGHT)

result_image = Image.alpha_composite(background_image, text_image).convert("RGB")


def _display_debug(inky, image):
    image = dithered(inky, image)
    image.show()


def _display_frame(inky, image):
    if random.randint(0, 5) == 3:
        log("Clear frame")
        clear(inky)
    log("Show image")
    inky.set_image(image, saturation=SATURATION)
    inky.show()
    log("Done")


if DEBUG:
    _display_debug(inky, result_image)
else:
    _display_frame(inky, result_image)
