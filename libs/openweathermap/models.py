from dataclasses import dataclass, field
from typing import Optional, List, Dict

from dataclasses_json import dataclass_json, config

from bot.proto.database import UserSettings
from libs.helpers import cast_or


@dataclass_json
@dataclass
class Condition:
    id: int
    main: str
    description: str
    icon: str


class Temperature(float):
    def convert(self, settings: UserSettings) -> "Temperature":
        return self if settings.imperial else (self - 32) / 1.8


class Speed(float):
    def convert(self, settings: UserSettings) -> "Speed":
        return self if settings.imperial else self * 1.60934


class Distance(float):
    def convert(self, settings: UserSettings) -> "Distance":
        return self if settings.imperial else self * 1.60934


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
    _speed: float = field(metadata=config(field_name="speed"))
    direction: int = field(metadata=config(field_name="deg"))
    _gust: Optional[float] = field(metadata=config(field_name="gust"))

    @property
    def speed(self) -> Speed:
        return Speed(self._speed)

    @property
    def gust(self) -> Optional[Speed]:
        return Speed(self._gust)


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


@dataclass_json
@dataclass
class PollutionIndexResponseMain:
    aqi: int

    def __str__(self) -> str:
        return ("Good", "Fair", "Moderate", "Poor", "Very Poor")[self.aqi]


@dataclass_json
@dataclass
class PollutionIndexResponseComponents:
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float

    @property
    def levels(self) -> Dict[str, Optional[float]]:
        return {
            pretty_name: float(self.__dict__[field_name])
            for pretty_name, field_name in {
                "CO": "co",
                "NO": "no",
                "NO₂": "no2",
                "O₃": "o3",
                "SO₂": "so2",
                "Fine Particles": "pm2_5",
                "Coarse Particles": "pm10",
                "NH₃": "nh3",
            }.items()
        }


@dataclass_json
@dataclass
class PollutionIndexResponseData:
    dt: int
    main: PollutionIndexResponseMain
    components: PollutionIndexResponseComponents


@dataclass_json
@dataclass
class CurrentPollutionIndexResponse:
    coord: Coordinates
    list: List[PollutionIndexResponseData]

    @property
    def data(self) -> PollutionIndexResponseData:
        return self.list[0]
