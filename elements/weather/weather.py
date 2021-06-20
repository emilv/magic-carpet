import json
import os
import urllib.request
from datetime import datetime
from typing import cast
from dateutil.parser import isoparse

from .forecast_types import ForecastDict, ForecastData


def _get_forecasts(latitude, longitude) -> ForecastDict:
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={latitude}&lon={longitude}"
    print(url)
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

