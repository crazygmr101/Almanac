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

import math
from io import BytesIO
from typing import Tuple

import aiohttp
from PIL import Image
from expiringdict import ExpiringDict
from yarl import URL

from libs.openweathermap.errors import CityNotFoundError
from libs.openweathermap.models import CurrentConditionsResponse


class OpenWeatherMapAPI:
    def __init__(self, token):
        self.token: str = token
        self._cache = ExpiringDict(max_len=1000, max_age_seconds=15 * 60)  # 15 mins

    async def get_current_conditions(self, latitude: float, longitude: float) -> CurrentConditionsResponse:
        latitude = round(latitude, 3)
        longitude = round(longitude, 3)
        res = self._cache.get((latitude, longitude), None)
        if res is not None:
            return res
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url=URL.build(
                    scheme="https",
                    host="api.openweathermap.org",
                    path="/data/2.5/weather",
                    query={
                        "appid": self.token,
                        "lat": latitude,
                        "lon": longitude,
                        "units": "imperial"
                    }
            )) as resp:
                r = await resp.json()
                if r["cod"] != 200:
                    raise CityNotFoundError
                res = CurrentConditionsResponse.from_json(await resp.read())
                self._cache[(latitude, longitude)] = res
                return res

    def get_tile(self, lat: float, lon: float, zoom: int) -> Tuple[int, int]:
        n = 2.0 ** zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi) / 2.0 * n)
        return x, y

    async def radar_image(self, latitude: float, longitude: float, zoom: int, layer: str) -> Image.Image:
        x, y = self.get_tile(latitude, longitude, zoom)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url=URL.build(
                    scheme="https",
                    host="tile.openweathermap.org",
                    path=f"/map/{layer}/{zoom}/{x}/{y}.png",
                    query={
                        "appid": self.token
                    }
            )) as resp:
                buf = BytesIO()
                buf.write(await resp.read())
        buf.seek(0)
        img: Image.Image = Image.open(buf)
        img.load()
        return img
