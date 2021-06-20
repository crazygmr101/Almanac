"""
Copyright 2021 crazygmr101

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class WeatherGovUnitValue:
    value: float
    unit_code: str = field(metadata=config(field_name="unitCode"))


@dataclass_json
@dataclass
class WeatherGovRLProperties:
    city: str
    state: str
    distance: WeatherGovUnitValue
    bearing: WeatherGovUnitValue


@dataclass_json
@dataclass
class WeatherGovRelativeLocation:
    type: str
    properties: WeatherGovRLProperties


@dataclass_json
@dataclass
class WeatherGovPointProperties:
    cwa: str
    grid_id: str = field(metadata=config(field_name="gridId"))
    grid_x: int = field(metadata=config(field_name="gridX"))
    grid_y: int = field(metadata=config(field_name="gridY"))
    forecast_url: str = field(metadata=config(field_name="forecast"))
    forecast_hourly_url: str = field(metadata=config(field_name="forecastHourly"))
    forecast_grid_url: str = field(metadata=config(field_name="forecastGridData"))
    observation_stations_url: str = field(metadata=config(field_name="observationStations"))
    forecast_zone_url: str = field(metadata=config(field_name="forecastZone"))
    county_url: str = field(metadata=config(field_name="county"))
    fire_weather_zone_url: str = field(metadata=config(field_name="fireWeatherZone"))
    timezone: str = field(metadata=config(field_name="timeZone"))
    relative_location: WeatherGovRelativeLocation = field(metadata=config(field_name="relativeLocation"))
    radar_station: str = field(metadata=config(field_name="radarStation"))


@dataclass_json
@dataclass
class WeatherGovPoint:
    properties: WeatherGovPointProperties
    id: str
