from dataclasses import dataclass, field
from typing import Optional, List

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Condition:
    id: int
    main: str
    description: str
    icon: str


class Temperature(float):
    def to(self, unit: str):
        return self if unit == "f" else (self - 32) / 1.8


@dataclass_json
@dataclass
class DetailedCondition:
    _temp: float = field(metadata=config(field_name="temp"))
    _feels_like: float = field(metadata=config(field_name="feels_like"))
    temp_min: float
    temp_max: float
    pressure: float
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    @property
    def temp(self) -> Temperature:
        return Temperature(self._temp)

    @property
    def feels_like(self) -> Temperature:
        return Temperature(self._feels_like)


@dataclass_json
@dataclass
class Wind:
    speed: float
    direction: int = field(metadata=config(field_name="deg"))
    gust: Optional[float] = None


@dataclass_json
@dataclass
class Clouds:
    all: float


@dataclass_json
@dataclass
class Precipitation:
    one_hour: float = field(metadata=config(field_name="1h"))
    three_hour: float = field(metadata=config(field_name="3h"))


@dataclass_json
@dataclass
class SysData:
    sunrise: int
    sunset: int
    country: Optional[str] = ""


@dataclass_json
@dataclass
class Coordinates:
    lat: int
    lon: int


@dataclass_json
@dataclass
class CurrentConditionsResponse:
    coord: Coordinates
    weather: List[Condition]
    main: DetailedCondition
    visibility: float
    wind: Wind
    clouds: Clouds
    dt: int
    sys: SysData
    timezone: int
    city_id: int = field(metadata=config(field_name="id"))
    city_name: int = field(metadata=config(field_name="name"))
    rain: Optional[Precipitation] = None
    snow: Optional[Precipitation] = None
