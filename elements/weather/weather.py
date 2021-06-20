import json
import os
import urllib.request
from collections import namedtuple
from datetime import datetime
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


Temperatures = namedtuple("Temperatures", ("min", "max"))


def _temperatures(forecast: ForecastData) -> Temperatures:
    temp_max = forecast["next_6_hours"]["details"]["air_temperature_max"]
    temp_min = forecast["next_6_hours"]["details"]["air_temperature_min"]
    return Temperatures(temp_min, temp_max)


def _stitch(forecast: ForecastData, width: int, height: int) -> Image:
    backdrop_color = (255, 140, 0)
    ellipse_dimensions = (126, 105)
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
    backdrop.paste(rotated_ellipse, ellipse_placement)

    # Time for the weather symbol
    symbol_code = _symbol(forecast)
    Image.open(f"yr-weather-symbols/")

    backdrop.show()
