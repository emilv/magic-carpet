import time

from inky.inky_uc8159 import Inky


def clear(inky: Inky):
    for y in range(inky.height - 1):
        for x in range(inky.width - 1):
            inky.set_pixel(x, y, Inky.CLEAN)
    inky.show()
    time.sleep(0.8)


if __name__ == "__main__":
    inky = Inky()
    clear(inky)
