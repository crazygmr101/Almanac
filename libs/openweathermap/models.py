from dataclasses import dataclass, field
from typing import Optional, List

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Coordinates:
    lon: int
    lat: int


@dataclass_json
@dataclass
class Condition:
    id: int
    main: str
    description: str
    icon: str


@dataclass_json
@dataclass
class DetailedCondition:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


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
    country: str
    sunrise: int
    sunset: int


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
