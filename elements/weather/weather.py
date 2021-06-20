import json
import os
import urllib.request
from collections import namedtuple
from datetime import datetime, timezone
from typing import Tuple, cast

from PIL import Image, ImageDraw
from dateutil.parser import isoparse

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
    backdrop_color = (0, 0, 0)
    ellipse_dimensions = (126, 105)
    symbol_dimensions = (105, 105)
    center_x, center_y = (500, 100)

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
    backdrop.paste(rotated_ellipse, ellipse_placement, mask=rotated_ellipse)

    # Time for the weather symbol
    symbol_code = _symbol(forecast)
    symbol = _symbol_image(symbol_code).resize(symbol_dimensions)
    symbol_placement = (
        center_x - symbol.width // 2,
        center_y - symbol.height // 2 - 20,
    )
    backdrop.paste(symbol, symbol_placement, mask=symbol)

    return backdrop


def get_image(width: int, height: int) -> Image:
    forecasts = _get_forecasts(os.getenv("WEATHER_LAT"), os.getenv("WEATHER_LON"))
    forecast = _forecast_at_time(forecasts, datetime.now(timezone.utc))
    return _stitch(forecast, width, height)
