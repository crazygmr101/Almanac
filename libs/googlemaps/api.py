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
from yarl import URL

from libs.googlemaps.models import GeocodeResponse


class GoogleMapsAPI:
    def __init__(self, token):
        self.token = token
        self._cache = ExpiringDict(10000, 60 * 60 * 12)  # 12h

    async def geocode(self, location: str) -> GeocodeResponse:
        res = self._cache.get(location, None)
        if res is not None:
            return res
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                url=URL.build(
                    host="maps.googleapis.com",
                    scheme="https",
                    path="/maps/api/geocode/json",
                    query={"address": location, "key": self.token},
                )
            ) as resp:
                r = await resp.json()
                res = GeocodeResponse.from_json(json.dumps(r))
                self._cache[location] = res
                return res
