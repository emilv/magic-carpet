import random
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from inky.inky_uc8159 import Inky

import color_fit
from clear import clear
from utils import dithered, get_image, log, WIDTH, HEIGHT, SATURATION

IMAGES = 4
FONTNAME = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
TEXTMARGIN = 5
DEBUG = len(sys.argv) > 1 and sys.argv[1] == "debug"

inky = Inky()


def _get_enhanced_image() -> Image:
    image = get_image().convert("RGB")

    # Make it "pop"
    enhance = ImageEnhance.Contrast(image)
    return enhance.enhance(2)


with ThreadPoolExecutor(max_workers=IMAGES) as executor:
    images = list(executor.map(lambda _: _get_enhanced_image(), range(IMAGES)))

image = None
best_score = float("inf")
for i, current_image in enumerate(images):
    current_score = color_fit.color_fit(inky, current_image)
    log(f"Score: {current_score}")
    if current_score < best_score:
        log(f"Better. Using image {i}")
        image = current_image
        best_score = current_score

if DEBUG:
    image.show()

image = image.convert("RGB")
# image = Image.open("tomato.jpg")

# Dither image before converting to RGBA to make text outline smoother
# image = dithered(inky, image).convert("RGBA")
image = image.convert("RGBA")

# Draw text
text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(text_image)
# draw.fontmode = "1"  # Disable anti-aliasing

quote = "Fånga dagen"
while True:
    font_size = random.randint(45, 140)
    log(f"Font size: {font_size}")
    font = ImageFont.truetype(FONTNAME, size=font_size)
    text_width, text_height = font.getsize(quote, stroke_width=1)
    if text_width > WIDTH - 2 * TEXTMARGIN:
        log(f"Font size {font_size} results in width {text_width}. Trying again")
        continue
    break
text_x = random.randint(TEXTMARGIN, WIDTH - text_width - TEXTMARGIN)
text_y = random.randint(TEXTMARGIN, HEIGHT - text_height - TEXTMARGIN)
transparent = random.choice([True, False])
log(f"Transparent text: {transparent}")

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
    image = dithered(inky, image)
    image.show()
else:
    if random.randint(0, 5) == 2:
        log("Clearing image")
        clear(inky)
    log("Showing image")
    inky.set_image(image, saturation=SATURATION)
    inky.show()
    log("Done")
