import json
import os
import random
import urllib.request
from collections import namedtuple
from datetime import datetime, timezone
from typing import cast

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from dateutil.parser import isoparse

from outline import stroke
from .forecast_types import ForecastDict, ForecastData


def _get_forecasts(latitude, longitude) -> ForecastDict:
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={latitude}&lon={longitude}"
    req = urllib.request.Request(
        url=url, headers={"User-Agent": os.getenv("USER_AGENT")}
    )
    fd = urllib.request.urlopen(req)
    content = json.load(fd)
    return cast(ForecastDict, content)


def _forecast_at_time(forecasts: ForecastDict, at: datetime) -> ForecastData:
    for elem in forecasts["properties"]["timeseries"]:
        forecast_time = isoparse(elem["time"])
        if forecast_time >= at:
            return elem["data"]


def _symbol(forecast: ForecastData) -> str:
    return forecast["next_12_hours"]["summary"]["symbol_code"]


def _symbol_image(symbol: str) -> Image:
    # Bugs in Weathericon/2.0
    if symbol == "lightsleetshowersandthunder":
        symbol = "lightssleetshowersandthunder"
    elif symbol == "lightsnowshowersandthunder":
        symbol = "lightssnowshowersandthunder"

    try:
        image = Image.open(f"weathericons/png/{symbol}_day.png")
    except:
        image = Image.open(f"weathericons/png/{symbol}.png")

    return image


Temperatures = namedtuple("Temperatures", ("min", "max"))


def _temperatures(forecast: ForecastData) -> Temperatures:
    temp_max = forecast["next_6_hours"]["details"]["air_temperature_max"]
    temp_min = forecast["next_6_hours"]["details"]["air_temperature_min"]
    return Temperatures(temp_min, temp_max)


def _stitch(forecast: ForecastData, width: int, height: int) -> Image:
    font_name = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    font_color = (255, 255, 255)
    font_size = 25
    text_stroke_width = 3
    backdrop_color = (0, 0, 0)
    ellipse_dimensions = (126, 105)
    symbol_dimensions = (105, 105)
    center_x, center_y = random.choice([
        (500, 100),
        (500, 348),
        (100, 100),
        (100, 348),
    ])
    center_x += random.randint(-10, 10)
    center_y += random.randint(-10, 10)

    backdrop = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # An ellipse base
    ellipse = Image.new("RGBA", ellipse_dimensions)
    draw_ellipse = ImageDraw.Draw(ellipse)
    draw_ellipse.ellipse(((0, 0), ellipse_dimensions), fill=backdrop_color)
    rotated_ellipse = ellipse.rotate(-45, expand=True)
    ellipse_placement = (
        center_x - rotated_ellipse.width // 2,
        center_y - rotated_ellipse.height // 2,
    )
    backdrop.alpha_composite(rotated_ellipse, ellipse_placement)

    # Weather symbol
    symbol_code = _symbol(forecast)
    symbol_raw = _symbol_image(symbol_code).resize(symbol_dimensions)
    stroke1 = stroke(symbol_raw, threshold=0, stroke_size=3, color=(0, 0, 0))
    symbol = stroke1

    symbol_placement = (
        center_x - symbol.width // 2,
        center_y - symbol.height // 2 - 20,
    )
    backdrop.alpha_composite(symbol, symbol_placement)

    # Temperature
    text_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_image)
    temperatures = _temperatures(forecast)
    if abs(temperatures.min - temperatures.max) < 2:
        text = f"{temperatures.min:.0f} ???"
    else:
        text = f"{temperatures.min:.0f} - {temperatures.max:.0f} ???"
    font = ImageFont.truetype(font_name, size=font_size)
    text_width, text_height = font.getsize(text, stroke_width=text_stroke_width)
    text_placement = (center_x - text_width // 2 + 3, center_y + 14)
    text_draw.text(
        text_placement,
        text,
        fill=font_color,
        font=font,
        stroke_width=text_stroke_width,
        stroke_fill=(0, 0, 0),
    )
    backdrop.alpha_composite(text_image)

    return backdrop


def get_image(width: int, height: int) -> Image:
    forecasts = _get_forecasts(os.getenv("WEATHER_LAT"), os.getenv("WEATHER_LON"))
    forecast = _forecast_at_time(forecasts, datetime.now(timezone.utc))
    return _stitch(forecast, width, height)
