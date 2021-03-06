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
import json

import aiohttp
from expiringdict import ExpiringDict

from libs.weather_gov.models import WeatherGovPoint


# noinspection PyMethodMayBeStatic
class WeatherGovAPI:
    def __init__(self):
        self._cache = ExpiringDict(
            max_len=1000, max_age_seconds=60 * 60 * 12
        )  # expire in 12h

    async def lookup_point(
        self, latitude: float, longitude: float
    ) -> WeatherGovPoint:
        latitude = round(latitude, 3)
        longitude = round(longitude, 3)
        res = self._cache.get((latitude, longitude), None)
        if res is not None:
            return res
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                f"https://api.weather.gov/points/{latitude},{longitude}"
            ) as resp:
                resp.raise_for_status()  # TODO intelligent errors here
                content = json.dumps(await resp.json())
                res = WeatherGovPoint.from_json(content)
                self._cache[(latitude, longitude)] = res
                return res
