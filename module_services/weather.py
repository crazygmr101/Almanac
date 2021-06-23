import os
from datetime import datetime
from io import BytesIO
from typing import Union

import aiohttp
import discord

from libs.maptiler import MapTilerAPI
from libs.openweathermap import OpenWeatherMapAPI
from libs.weather_gov import WeatherGovAPI
from module_services.bot import BotService
from module_services.geocoding import GeocodingService


# noinspection PyMethodMayBeStatic
class WeatherService(BotService, GeocodingService):
    def __init__(self):
        super(WeatherService, self).__init__()
        self.owm_api = OpenWeatherMapAPI(os.getenv("OWM"))
        self.weather_gov_api = WeatherGovAPI()
        self.map_api = MapTilerAPI(os.getenv("MAPTILER"))

    async def current_conditions(self, city: str) -> discord.Embed:
        lat, lon = await self.parse_location(city)
        try:
            data = (await self.weather_gov_api.lookup_point(lat, lon)).properties
        except aiohttp.ClientResponseError as e:
            return self.error_embed(title="Lookup error", description=e.message)
        conditions = await self.owm_api.get_current_conditions(lat, lon)
        sunrise = datetime.utcfromtimestamp(conditions.sys.sunrise + conditions.timezone).strftime("%-I:%M %p")
        sunset = datetime.utcfromtimestamp(conditions.sys.sunset + conditions.timezone).strftime("%-I:%M %p")
        embed = self.ok_embed(title=f"**Conditions for {conditions.city_name}, {conditions.sys.country}**\n",
                              description=f"🏙 {conditions.weather[0].description.title()}\n"
                                          f"🌡️ **{int(conditions.main.temp)}**°F "
                                          f"(feels like **{int(conditions.main.feels_like)}**°)\n"
                                          f"🌅 **Sunrise**: {sunrise}\n"
                                          f"🌇 **Sunset**: {sunset}\n"
                                          f"🌬️ **{int(conditions.wind.speed)}** MPH from "
                                          f"{self.direction_for(conditions.wind.direction)}") \
            .set_thumbnail(url=self.icon_url_for(conditions.weather[0].icon)) \
            .set_footer(text=f"Powered by OpenWeatherMap | {round(lat, 4)} {round(lon, 4)}")
        if conditions.snow:
            embed = embed.add_field(name="Snowfall", inline=True,
                                    value=f"❄️️ **1 hour**: {round(conditions.snow.one_hour, 2)} in"
                                          f"🌨️ **3 hour**: {round(conditions.snow.three_hour, 2)} in")
        if conditions.rain:
            embed = embed.add_field(name="Rainfall", inline=True,
                                    value=f"💧 **1 hour**: {round(conditions.rain.one_hour, 1)} in"
                                          f"🌧 **3 hour**: {round(conditions.rain.three_hour, 1)} in")
        return embed

    async def radar_map(self, city: str) -> discord.Embed:
        lat, lon = await self.parse_location(city)
        try:
            data = (await self.weather_gov_api.lookup_point(lat, lon)).properties
        except aiohttp.ClientResponseError as e:
            return self.error_embed(title="Lookup error", description=e.message)
        conditions = await self.owm_api.get_current_conditions(lat, lon)
        if data.radar_station:
            embed = self.ok_embed(title=f"**Radar for {conditions.city_name}, {conditions.sys.country}**",
                                  description=f"{round(lat, 4)}° {round(lon, 4)}°")
            embed.set_image(url=f"https://radar.weather.gov/ridge/lite/{data.radar_station}_loop.gif")
        else:
            embed = self.error_embed(title="No radar data available",
                                     description=f"No radar data was available for the requested location")
        return embed

    def icon_url_for(self, icon: str) -> str:
        return f"http://openweathermap.org/img/wn/{icon}@2x.png"

    def direction_for(self, deg: Union[int, float]):
        # see https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f#gistcomment-3070256
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(deg / (360. / len(dirs)))
        return dirs[ix % len(dirs)]

    async def point_data(self, lat: float, lon: float) -> discord.Embed:
        try:
            data = (await self.weather_gov_api.lookup_point(lat, lon)).properties
        except aiohttp.ClientResponseError as e:
            return self.error_embed(title="Lookup error", description=e.message)
        miles = round(data.relative_location.properties.distance.value / 1609.34, 1)
        relative_location = f"{data.relative_location.properties.city}, " \
                            f"{data.relative_location.properties.state}"
        if miles > 0.5:
            relative_location = f"{miles} mi " \
                                f"{self.direction_for(data.relative_location.properties.bearing.value)} of " + \
                                relative_location
        embed = self.ok_embed(title=f"Point Lookup {data.grid_x},{data.grid_y}",
                              description=f":satellite: **Radar**: {data.radar_station}\n"
                                          f":pushpin: **Location**: {relative_location}")
        return embed

    async def weather_map(self, city: str, zoom: int, layer: str) -> discord.File:
        lat, lon = await self.parse_location(city)
        buf = BytesIO()
        layer_img = await self.owm_api.radar_image(lat, lon, zoom, layer)
        osm_img = await self.map_api.get_map_image(lat, lon, zoom)
        osm_img.alpha_composite(layer_img)
        osm_img.save(buf, format="png")
        buf.seek(0)
        return discord.File(buf, "radar.png")
