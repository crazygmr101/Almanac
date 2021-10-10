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
import os
from datetime import datetime

import aiohttp
from expiringdict import ExpiringDict
from yarl import URL

from libs.googlemaps.models import GeocodeResponse
from libs.nasa.models import APOD


class NasaAPI:
    def __init__(self):
        self.token = os.getenv("NASA")
        self._apod_cache = ExpiringDict(10000, 60 * 60 * 12)  # 12h

    def _route(self, path: str, **kwargs) -> URL:
        kwargs.update({"api_key": self.token})
        return URL.build(
            scheme="https",
            host="api.nasa.gov",
            path=path,
            query=kwargs,
        )

    async def apod(self, date: datetime) -> APOD:
        if (date.year, date.month, date.day) not in self._apod_cache:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    url=self._route(
                        "/planetary/apod",
                        date=f"{date.year:0>4}-{date.month:0>2}-{date.day:0>2}",
                    )
                ) as resp:
                    self._apod_cache[
                        (date.year, date.month, date.day)
                    ] = APOD.from_json(await resp.read())
        return self._apod_cache[(date.year, date.month, date.day)]
