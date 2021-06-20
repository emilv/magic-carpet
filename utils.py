import datetime
import io
import random
import urllib.request
from enum import Enum

import hitherdither
from PIL import Image
from inky.inky_uc8159 import Inky

WIDTH, HEIGHT = 600, 448
SATURATION = 0.8

start_log = datetime.datetime.now()
last_log = start_log


def log(msg: str) -> None:
    global last_log
    now = datetime.datetime.now()
    diff = (now - last_log).total_seconds()
    from_start = (now - start_log).total_seconds()
    last_log = now
    print(f"[{from_start:5.2f} +{diff:.2f} ]\t{msg}")


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


class DitheringModes(Enum):
    DEFAULT = "default"
    SMALL_DOTS = "small_dots"
    LARGE_DOTS = "large_dots"


def dithered(
    inky: Inky, image: Image, mode: DitheringModes = DitheringModes.DEFAULT
) -> Image:
    log("Dithering")
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
    log("Done dithering")
    return image_dithered


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
