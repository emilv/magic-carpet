from typing import List, Union
from typing_extensions import TypedDict

_Number = Union[int, float]


class InstantDetails(TypedDict, total=False):
    cloud_area_fraction_high: _Number
    wind_speed_percentile_90: _Number
    wind_speed_percentile_10: _Number
    air_temperature_percentile_10: _Number
    wind_speed_of_gust: _Number
    wind_speed: _Number
    ultraviolet_index_clear_sky: _Number
    air_pressure_at_sea_level: _Number
    fog_area_fraction: _Number
    air_temperature_percentile_90: _Number
    dew_point_temperature: _Number
    air_temperature: _Number
    wind_from_direction: _Number
    cloud_area_fraction_low: _Number
    relative_humidity: _Number
    cloud_area_fraction_medium: _Number
    cloud_area_fraction: _Number


class Instant(TypedDict):
    details: InstantDetails


class NextHoursDetails(TypedDict, total=False):
    probability_of_precipitation: _Number
    air_temperature_max: _Number
    air_temperature_min: _Number
    precipitation_amount_max: _Number
    precipitation_amount_min: _Number
    precipitation_amount: _Number


class NextHoursSummary(TypedDict):
    symbol_code: str


class NextHours(TypedDict):
    details: NextHoursDetails
    summary: NextHoursSummary


class ForecastData(TypedDict, total=False):
    instant: Instant
    next_1_hours: NextHours
    next_6_hours: NextHours
    next_12_hours: NextHours


class ForecastTimeseriesElement(TypedDict):
    data: ForecastData
    time: str


class ForecastGeometry(TypedDict):
    type: str
    coordinates: List[float]


class ForecastMetaUnits(TypedDict):
    fog_area_fraction: str  # %
    wind_speed_percentile_90: str  # m/s
    air_temperature_percentile_90: str  # "celsius"
    precipitation_amount_min: str  # "mm"
    cloud_area_fraction_high: str  # "%"
    precipitation_amount: str  # "mm"
    precipitation_amount_max: str  # "mm"
    probability_of_precipitation: str  # "%"
    wind_speed_percentile_10: str  # "m/s"
    dew_point_temperature: str  # "celsius"
    wind_speed_of_gust: str  # "m/s"
    air_temperature_max: str  # celsius"
    cloud_area_fraction_low: str  # "%"
    air_temperature_percentile_10: str  # "celsius"
    ultraviolet_index_clear_sky: str  # "1"
    air_temperature: str  # "celsius"
    wind_speed: str  # "m/s"
    wind_from_direction: str  # "degrees"
    relative_humidity: str  # "%"
    probability_of_thunder: str  # "%"
    cloud_area_fraction: str  # "%"
    air_pressure_at_sea_level: str  # "hPa"
    air_temperature_min: str  # "celsius"
    cloud_area_fraction_medium: str  # "%#


class ForecastMeta(TypedDict):
    units: ForecastMetaUnits
    updated_at: str


class Properties(TypedDict):
    meta: ForecastMeta
    timeseries: List[ForecastTimeseriesElement]


class ForecastDict(TypedDict):
    geometry: ForecastGeometry
    properties: Properties
