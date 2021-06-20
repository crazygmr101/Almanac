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
import os
import re
from typing import Tuple, Optional

from libs.googlemaps import GoogleMapsAPI


# noinspection PyMethodMayBeStatic
class GeocodingService:
    def __init__(self):
        self.gmaps_api = GoogleMapsAPI(os.getenv("GMAPS"))

    async def parse_location(self, location) -> Tuple[float, float]:
        # try to parse lat/long first
        res = self.try_parse_lat_long(location)
        if res is not None:
            return res

        # try to geocode with google maps
        res = (await self.gmaps_api.geocode(location)).results[0].geometry.location
        return res.lat, res.lon

    def try_parse_lat_long(self, value: str) -> Optional[Tuple[float, float]]:
        value = value.replace("°", "")
        value = re.sub(r"\s([news])", "$1", value.lower())
        if len(value.split(" ")) != 2:
            return None
        lat, lon = tuple(value.split(" "))
        try:
            lat = (-1. if lat.endswith("s") else 1.) * float(re.sub("[ns]", "", lat))
        except ValueError:
            return None
        try:
            lon = (-1. if lon.endswith("w") else 1.) * float(re.sub("[ew]", "", lon))
        except ValueError:
            return None
        return lat, lon
