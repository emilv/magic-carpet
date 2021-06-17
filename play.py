import datetime
import random
import sys
import io
import urllib.request
from enum import Enum

import hitherdither
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from inky.inky_uc8159 import Inky

WIDTH, HEIGHT = 600, 448
SATURATION = 0.8
FONTNAME = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
TEXTMARGIN = 5
DEBUG = len(sys.argv) > 1 and sys.argv[1] == "debug"

last_log = datetime.datetime.now()


def _log(msg: str) -> None:
    global last_log
    now = datetime.datetime.now()
    diff = (now - last_log).total_seconds()
    last_log = now
    print(f"[+{diff:.2f}]\t{msg}")


def _image() -> io.BytesIO:
    _log("Download image")
    fd = urllib.request.urlopen(f"https://source.unsplash.com/random/{WIDTH}x{HEIGHT}")
    content = fd.read()
    _log("Image downloaded")
    return io.BytesIO(content)


class DitheringModes(Enum):
    DEFAULT = "default"
    SMALL_DOTS = "small_dots"
    LARGE_DOTS = "large_dots"


def _dithered(
    inky: Inky, image: Image, mode: DitheringModes = DitheringModes.DEFAULT
) -> Image:
    _log("Dithering")
    palette = hitherdither.palette.Palette(
        inky._palette_blend(SATURATION, dtype="uint24")
    )
    thresholds = [64, 64, 64]  # Threshold for snapping colours, I guess?
    if mode == DitheringModes.SMALL_DOTS:
        image_dithered = hitherdither.ordered.cluster.cluster_dot_dithering(
            image, palette, thresholds, order=4
        )
    elif mode == DitheringModes.LARGE_DOTS:
        image_dithered = hitherdither.ordered.cluster.cluster_dot_dithering(
            image, palette, thresholds, order=8
        )
    else:
        image_dithered = hitherdither.ordered.bayer.bayer_dithering(
            image, palette, thresholds, order=8
        )
    _log("Done dithering")
    return image_dithered


def _clear(inky: Inky):
    if DEBUG:
        return
    for y in range(inky.height - 1):
        for x in range(inky.width - 1):
            inky.set_pixel(x, y, Inky.CLEAN)
    inky.show()


inky = Inky()

image = Image.open(_image()).convert("RGBA")
# image = Image.open("tomato.jpg")

# Make it "pop"
enhance = ImageEnhance.Contrast(image)
image = enhance.enhance(2)

# Draw text
text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(text_image)

quote = "Fånga dagen"
while True:
    font_size = random.randint(45, 140)
    _log(f"Font size: {font_size}")
    font = ImageFont.truetype(FONTNAME, size=font_size)
    text_width, text_height = font.getsize(quote, stroke_width=1)
    if text_width > WIDTH - 2 * TEXTMARGIN:
        _log(f"Font size {font_size} results in width {text_width}. Trying again")
        continue
    break
text_x = random.randint(TEXTMARGIN, WIDTH - text_width - TEXTMARGIN)
text_y = random.randint(TEXTMARGIN, HEIGHT - text_height - TEXTMARGIN)
transparent = random.choice([True, False])
_log(f"Transparent text: {transparent}")

draw.text(
    (text_x, text_y),
    quote,
    fill=(255, 255, 255, 150 if transparent else 255),
    font=font,
    stroke_width=1,
    stroke_fill=(0, 0, 0),
)

image = Image.alpha_composite(image, text_image)
image = image.convert("RGB")

if DEBUG:
    image = _dithered(inky, image)
    image.show()
else:
    if random.randint(0, 5) == 2:
        _log("Clearing image")
        _clear(inky)
    _log("Showing image")
    inky.set_image(image, saturation=SATURATION)
    inky.show()
    _log("Done")
