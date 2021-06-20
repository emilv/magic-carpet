import os
from datetime import datetime, timezone
from pprint import pprint

from dotenv import load_dotenv

from elements.weather.weather import _forecast_at_time, _get_forecasts, _stitch, _symbol, _temperatures
from utils import HEIGHT, WIDTH

load_dotenv()
forecasts = _get_forecasts(os.getenv('WEATHER_LAT'), os.getenv('WEATHER_LON'))
forecast = _forecast_at_time(forecasts, datetime.now(timezone.utc))
symbol = _symbol(forecast)
temperatures = _temperatures(forecast)
pprint(symbol)
pprint(temperatures)
image = _stitch(forecast, WIDTH, HEIGHT)
image.show()
