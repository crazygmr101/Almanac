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
from datetime import datetime
from typing import List, Union

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class _Weather:
    id: int
    main: str
    description: str
    icon: str


@dataclass_json
@dataclass
class _Precipitation:
    one_hour: float = field(metadata=config(field_name="1h"), default=0)
    three_hour: float = field(metadata=config(field_name="3h"), default=0)


@dataclass_json
@dataclass
class _CurrentCondition:
    dt: int
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    _weather: List[_Weather] = field(metadata=config(field_name="weather"))
    wind_gust: float = field(default=None)
    rain: _Precipitation = field(default=_Precipitation(0, 0))
    snow: _Precipitation = field(default=_Precipitation(0, 0))

    @property
    def weather(self) -> _Weather:
        return self._weather[0]


@dataclass_json
@dataclass
class _HourlyCondition:
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    pop: Union[int, float]
    _weather: List[_Weather] = field(metadata=config(field_name="weather"))
    rain: _Precipitation = field(default=_Precipitation(0, 0))
    snow: _Precipitation = field(default=_Precipitation(0, 0))
    wind_gust: float = field(default=None)

    @property
    def weather(self) -> _Weather:
        return self._weather[0]


@dataclass_json
@dataclass
class _DailyTemperature:
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


@dataclass_json
@dataclass
class _DailyFeelsLike:
    day: float
    night: float
    eve: float
    morn: float


@dataclass_json
@dataclass
class _DailyCondition:
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    temp: _DailyTemperature
    feels_like: _DailyFeelsLike
    pressure: int
    humidity: int
    dew_point: int
    wind_speed: float
    wind_deg: int
    clouds: int
    pop: Union[int, float]
    _weather: List[_Weather] = field(metadata=config(field_name="weather"))
    rain: float = field(default=0)  # mm
    snow: float = field(default=0)  # mm

    @property
    def weather(self) -> _Weather:
        return self._weather[0]

    def __str__(self) -> str:
        return f"{datetime.fromtimestamp(self.dt).isoformat()} {self.temp.min}/{self.temp.max} {self.clouds}"


@dataclass_json
@dataclass
class _WeatherAlert:
    sender_name: str
    event: str
    start: int
    end: int
    description: str
    tags: List[str]


@dataclass_json()
@dataclass
class OneCallAPIResponse:
    latitude: float = field(metadata=config(field_name="lat"))
    longitude: float = field(metadata=config(field_name="lon"))
    timezone: str
    timezone_offset: int
    current: _CurrentCondition
    hourly: List[_HourlyCondition]
    daily: List[_DailyCondition]
    alerts: List[_WeatherAlert] = field(default_factory=lambda: [])
