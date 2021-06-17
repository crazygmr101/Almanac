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

import json
from types import SimpleNamespace
from typing import TYPE_CHECKING

import aiohttp
from yarl import URL

from libs.openweathermap.errors import CityNotFoundError
from libs.openweathermap.models import CurrentConditionsResponse


class OpenWeatherMapAPI:
    def __init__(self, token):
        self.token: str = token

    async def get_current_conditions(self, city: str) -> CurrentConditionsResponse:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url=URL.build(
                    scheme="https",
                    host="api.openweathermap.org",
                    path="/data/2.5/weather",
                    query={
                        "appid": self.token,
                        "q": city,
                        "units": "imperial"
                    }
            )) as resp:
                r = await resp.json()
                if r["cod"] != 200:
                    raise CityNotFoundError
                return CurrentConditionsResponse.from_json(await resp.read())
