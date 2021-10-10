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
from __future__ import annotations

from datetime import timedelta
from io import BytesIO
from typing import Tuple

import aiohttp
from PIL import Image
from expiringdict import ExpiringDict
from yarl import URL

from libs.disk_cache import DiskCache
from libs.helpers import get_tiles, assemble_mosaic
from libs.openweathermap.errors import CityNotFoundError
from libs.openweathermap.models import (
    CurrentConditionsResponse,
    CurrentPollutionIndexResponse,
    ForecastResponse,
)


class OpenWeatherMapAPI:
    def __init__(self, token):
        self.token: str = token
        self._condition_cache = ExpiringDict(
            max_len=1000, max_age_seconds=15 * 60
        )  # 15 mins
        self._pollution_cache = ExpiringDict(
            max_len=1000, max_age_seconds=15 * 60
        )  # 15 mins
        self.disk_cache = DiskCache(
            "/tmp/almanac/weather-maps/", timedelta(minutes=15)
        )

    def _route(self, path: str, **kwargs) -> URL:
        kwargs.update({"appid": self.token})
        return URL.build(
            scheme="https",
            host="api.openweathermap.org",
            path=path,
            query=kwargs,
        )

    async def get_forecast(
        self, latitude: float, longitude: float
    ) -> ForecastResponse:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                url=self._route(
                    "/data/2.5/forecast",
                    lat=latitude,
                    lon=longitude,
                    units="imperial",
                )
            ) as resp:
                forecast: ForecastResponse = ForecastResponse.from_json(
                    await resp.read()
                )
                if forecast.status_code != 200:
                    raise CityNotFoundError
                return forecast

    async def get_current_weather(
        self, latitude: float, longitude: float
    ) -> CurrentConditionsResponse:
        latitude = round(latitude, 3)
        longitude = round(longitude, 3)
        conditions = self._condition_cache.get((latitude, longitude), None)
        if conditions:
            return conditions
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                url=self._route(
                    "/data/2.5/weather",
                    lat=latitude,
                    lon=longitude,
                    units="imperial",
                )
            ) as resp:
                r = await resp.json()
                if r["cod"] != 200:
                    raise CityNotFoundError
                conditions: CurrentConditionsResponse = (
                    CurrentConditionsResponse.from_json(await resp.read())
                )
                self._condition_cache[(latitude, longitude)] = conditions
        return conditions

    async def get_current_pollution(
        self, latitude: float, longitude: float
    ) -> CurrentPollutionIndexResponse:
        latitude = round(latitude, 3)
        longitude = round(longitude, 3)
        pollution = self._pollution_cache.get((latitude, longitude), None)
        if pollution:
            return pollution
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                url=self._route(
                    "/data/2.5/air_pollution", lat=latitude, lon=longitude
                )
            ) as resp:
                pollution: CurrentPollutionIndexResponse = (
                    CurrentPollutionIndexResponse.from_json(await resp.read())
                )
            self._pollution_cache[(latitude, longitude)] = pollution
        return pollution

    async def get_current_conditions(
        self, latitude: float, longitude: float
    ) -> Tuple[CurrentConditionsResponse, CurrentPollutionIndexResponse]:
        return await self.get_current_weather(
            latitude, longitude
        ), await self.get_current_pollution(latitude, longitude)

    async def _radar_tile(
        self, x: int, y: int, zoom: int, layer: str
    ) -> Image.Image:
        resp = self.disk_cache.get(f"/{zoom}/{x}/{y}/{layer}.png")
        buf = BytesIO()
        if resp is not None:
            buf.write(resp)
            buf.seek(0)
        else:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    url=URL.build(
                        scheme="https",
                        host="tile.openweathermap.org",
                        path=f"/map/{layer}/{zoom}/{x}/{y}.png",
                        query={"appid": self.token},
                    )
                ) as resp:
                    buf = BytesIO()
                    buf.write(await resp.read())
                    buf.seek(0)
                    self.disk_cache.put(
                        f"/{zoom}/{x}/{y}/{layer}.png", buf.read()
                    )
                    buf.seek(0)
        img: Image.Image = Image.open(buf)
        img.load()
        return img

    async def radar_image(
        self, latitude: float, longitude: float, zoom: int, layer: str
    ) -> Image.Image:
        tiles, location = get_tiles(latitude, longitude, zoom)
        images = [
            await self._radar_tile(tile[0], tile[1], zoom, layer)
            for tile in [
                (tiles[0], tiles[1]),
                (tiles[0], tiles[3]),
                (tiles[2], tiles[1]),
                (tiles[2], tiles[3]),
            ]
        ]
        return assemble_mosaic(images, location)
