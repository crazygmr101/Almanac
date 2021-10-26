from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union

from dataclasses_json import config, DataClassJsonMixin

from bot.proto.database import UserSettings


@dataclass
class GenericResponse(DataClassJsonMixin):
    _status_code: Union[str, int] = field(metadata=config(field_name="cod"))

    @property
    def status_code(self) -> int:
        return int(self._status_code)


@dataclass
class Condition(DataClassJsonMixin):
    id: int
    main: str
    description: str
    icon: str


class Temperature(float):
    def convert(self, settings: UserSettings) -> float:
        return self if settings.imperial else (self - 32) / 1.8


class Speed(float):
    def convert(self, settings: UserSettings) -> float:
        return self if settings.imperial else self * 1.60934


class Distance(float):
    def convert(self, settings: UserSettings) -> float:
        return self if settings.imperial else self * 1.60934


@dataclass
class DetailedCondition(DataClassJsonMixin):
    _temp: float = field(metadata=config(field_name="temp"))
    _feels_like: float = field(metadata=config(field_name="feels_like"))
    temp_min: float
    temp_max: float
    pressure: float
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None
    description: Optional[str] = None

    @property
    def temp(self) -> Temperature:
        return Temperature(self._temp)

    @property
    def feels_like(self) -> Temperature:
        return Temperature(self._feels_like)


@dataclass
class Wind(DataClassJsonMixin):
    _speed: float = field(metadata=config(field_name="speed"))
    direction: int = field(metadata=config(field_name="deg"))
    _gust: Optional[float] = field(metadata=config(field_name="gust"))

    @property
    def speed(self) -> Speed:
        return Speed(self._speed)

    @property
    def gust(self) -> Optional[Speed]:
        # pyright makes me have the or 0 :SCWEEE:
        return Speed(self._gust or 0) if self._gust is not None else None


@dataclass
class Clouds(DataClassJsonMixin):
    all: float


@dataclass
class Precipitation(DataClassJsonMixin):
    one_hour: float = field(metadata=config(field_name="1h"), default=0)
    three_hour: float = field(metadata=config(field_name="3h"), default=0)


@dataclass
class SysData(DataClassJsonMixin):
    sunrise: int
    sunset: int
    country: Optional[str] = ""


@dataclass
class Coordinates(DataClassJsonMixin):
    lat: int
    lon: int


@dataclass
class CurrentConditionsResponse(DataClassJsonMixin):
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


@dataclass
class PollutionIndexResponseMain(DataClassJsonMixin):
    aqi: int

    def __str__(self) -> str:
        return ("Good", "Fair", "Moderate", "Poor", "Very Poor")[self.aqi]


@dataclass
class PollutionIndexResponseComponents(DataClassJsonMixin):
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


@dataclass
class PollutionIndexResponseData(DataClassJsonMixin):
    dt: int
    main: PollutionIndexResponseMain
    components: PollutionIndexResponseComponents


@dataclass
class CurrentPollutionIndexResponse(DataClassJsonMixin):
    coord: Coordinates
    list: List[PollutionIndexResponseData]

    @property
    def data(self) -> PollutionIndexResponseData:
        return self.list[0]


@dataclass
class ForecastResponseData(DataClassJsonMixin):
    dt: int
    main: DetailedCondition
    clouds: Clouds
    wind: Wind
    precip_chance: float = field(metadata=config(field_name="pop"))
    rain: Optional[Precipitation] = None
    snow: Optional[Precipitation] = None


@dataclass
class ForecastResponse(GenericResponse, DataClassJsonMixin):
    list: List[ForecastResponseData] = field(default_factory=lambda: [])
