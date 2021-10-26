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
from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json, DataClassJsonMixin


@dataclass
class Coordinates(DataClassJsonMixin):
    lat: int
    lng: int

    @property
    def lon(self) -> int:
        return self.lng


@dataclass
class GoogleMapsGeometry(DataClassJsonMixin):
    location: Coordinates
    location_type: str


@dataclass
class GoogleMapsAddressComponent(DataClassJsonMixin):
    long_name: str
    short_name: str
    types: List[str]


@dataclass
class GoogleMapsAddress(DataClassJsonMixin):
    address_components: List[GoogleMapsAddressComponent]
    formatted_address: str
    types: List[str]
    geometry: GoogleMapsGeometry


@dataclass
class GeocodeResponse(DataClassJsonMixin):
    status: str
    results: List[GoogleMapsAddress] = field(default_factory=lambda: [])
