import random

from PIL import Image, ImageDraw, ImageFont

from utils import log

TEXTMARGIN = 8
FONTNAME = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"


def get_carpe_diem(width: int, height: int) -> Image:
    # Draw text
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    # draw.fontmode = "1"  # Disable anti-aliasing

    quote = "Fånga dagen"
    while True:
        font_size = random.randint(45, 140)
        log(f"Font size: {font_size}")
        font = ImageFont.truetype(FONTNAME, size=font_size)
        text_width, text_height = font.getsize(quote, stroke_width=1)
        if text_width > width - 2 * TEXTMARGIN:
            log(f"Font size {font_size} results in width {text_width}. Trying again")
            continue
        break
    text_x = random.randint(TEXTMARGIN, width - text_width - TEXTMARGIN)
    text_y = random.randint(TEXTMARGIN, height - text_height - TEXTMARGIN)

    draw.text(
        (text_x, text_y),
        quote,
        fill=(255, 255, 255, 255),
        font=font,
        stroke_width=1,
        stroke_fill=(0, 0, 0),
    )

    return image
