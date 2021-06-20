import io
import time
import urllib.request

from PIL import Image, ImageEnhance
from inky.inky_uc8159 import Inky

import color_fit
from utils import HEIGHT, WIDTH, log

IMAGES = 3


def _get_enhanced_image() -> Image:
    image = get_image().convert("RGB")

    # Make it "pop"
    #return ImageEnhance.Contrast(image).enhance(1.4)
    return ImageEnhance.Color(image).enhance(1.5)


def get_best_image(inky: Inky) -> Image:
    images = []
    for _ in range(IMAGES):
        images.append(_get_enhanced_image())
        time.sleep(1.0)

    image = None
    best_score = float("inf")
    for i, current_image in enumerate(images):
        current_score = color_fit.color_fit(inky, current_image)
        log(f"Score: {current_score}")
        if current_score < best_score:
            log(f"Better. Using image {i}")
            image = current_image
            best_score = current_score

    return image.convert("RGBA")


def get_image() -> Image:
    log("Download background_image")
    try:
        fd = urllib.request.urlopen(f"https://source.unsplash.com/random/{WIDTH}x{HEIGHT}")
        content = fd.read()
        log("Image downloaded")
        return Image.open(io.BytesIO(content))
    except Exception as e:
        log(f"Failed download: {e}")
        return Image.open("tomato.jpg")
