from io import BytesIO
from typing import Union

import hikari

from bot.proto.database import UserSettings
from module_services.bot import BotService
from module_services.geocoding import GeocodingService


# noinspection PyMethodMayBeStatic
class WeatherServiceProto(BotService, GeocodingService):
    async def current_conditions(
        self, city: str, settings: UserSettings
    ) -> hikari.Embed:
        raise NotImplementedError

    async def radar_map(self, city: str) -> hikari.Embed:
        raise NotImplementedError

    def icon_url_for(self, icon: str) -> str:
        raise NotImplementedError

    def direction_for(self, deg: Union[int, float]):
        raise NotImplementedError

    async def point_data(self, lat: float, lon: float) -> hikari.Embed:
        raise NotImplementedError

    async def raw_weather_map(
        self, city: str, zoom: int, layer: str
    ) -> BytesIO:
        raise NotImplementedError

    async def weather_map(
        self, city: str, zoom: int, layer: str
    ) -> hikari.Embed:
        raise NotImplementedError

    MAP_TYPES = {"clouds", "precipitation", "pressure", "wind", "temperature"}
