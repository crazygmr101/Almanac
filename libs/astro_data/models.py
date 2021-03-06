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
import itertools
from dataclasses import dataclass
from functools import cached_property
from typing import List, TYPE_CHECKING, Tuple, Iterable, Set

if TYPE_CHECKING:
    from libs.astro_data import AstronomyClient

_TYPE_MAPPINGS = {
    "G": "Galaxy",
    "GX": "Galaxy",
    "AGX": "Active Galaxy",
    "RG": "Radio Galaxy",
    "IG": "Interacting Galaxy",
    "GC": "Globular Cluster",
    "OC": "Open Cluster",
    "NB": "Nebula",
    "PN": "Planetary Nebula",
    "DN": "Dark Nebula",
    "RN": "Reflection Nebula",
    "C+N": "Cluster associated with nebulosity",
    "HII": "HII Region",
    "SNR": "Supernova Remnant",
    "BN": "Bipolar Nebula",
    "EN": "Emission Nebula",
    "SA": "Stellar Association",
    "SC": "Star Cloud",
    "CL": "Cluster",
    "IR": "Infra-Red Object",
    "QSO": "Quasar",
    "Q?": "Possible Quasar",
    "ISM": "Interstellar Matter",
    "EMO": "Emission Object",
    "LIN": "LINEAR-type Active Galaxies",
    "BLL": "BL Lac Object",
    "BLA": "Blazar",
    "MOC": "Molecular Cloud",
    "YSO": "Young Stellar Object",
    "PN?": "Possible Planetary Nebula",
    "PPN": "Protoplanetary Nebula",
    "*": "Star",
    "**": "Double Star",
    "MUL": "Multiple Star",
    "empty": "Unknown",
}


@dataclass
class _Location:
    ra: float
    dec: float

    def __str__(self) -> str:
        return f"RA: {self.ra}  DEC: {self.dec}"


@dataclass
class _Magnitude:
    b: float
    v: float

    def __str__(self) -> str:
        return f"B: {self.b}  V: {self.v}"


@dataclass
class _Size:
    major: float
    minor: float

    def __str__(self) -> str:
        return f"{self.major} {self.minor}"


@dataclass
class _Redshift:
    value: float
    error: float

    def __str__(self) -> str:
        return f"{self.value} ERR: {self.error}"


@dataclass
class _Parallax:
    value: float
    error: float

    def __str__(self) -> str:
        return f"{self.value} ERR: {self.error}"


class DSO:
    def __init__(self, line: str):
        split = line.split("\t")

        self.id = int(split[0])
        self.location = _Location(float(split[1]), float(split[2]))
        self.magnitude = _Magnitude(float(split[3]), float(split[4]))
        self.type = split[5]
        self.morph_type = split[6]
        self.size = _Size(float(split[7]), float(split[8]))
        self.angle = float(split[9])
        self.redshift = _Redshift(float(split[10]), float(split[11]))
        self.parallax = _Parallax(float(split[12]), float(split[13]))

        self.ngc = int(split[16]) if split[16] else None
        self.ic = int(split[17]) if split[17] else None
        self.m = int(split[18]) if split[18] else None

        self.common_names = ""
        self.ned_notes = ""
        self.open_ngc_notes = ""
        self.constellation = ""

    def __str__(self) -> str:
        return (
            f"ID: {self.id}  TYPE: {_TYPE_MAPPINGS[self.type.upper()]}  MTYPE: {self.morph_type}\n"
            f"{self.location}  {self.constellation}\n"
            f"MAG: {self.magnitude}\n"
            f"SIZE: {self.size} @ {self.angle}\n"
            f"NGC: {self.ngc or '-'}  M: {self.m or '-'}\n"
            f"Common Name: {self.common_names or '-'}\n"
            f"NED Notes: {self.ned_notes or '-'}\n"
            f"OpenNGC Notes: {self.open_ngc_notes or '-'}\n"
        )

    @property
    def pretty_type(self) -> str:
        return _TYPE_MAPPINGS[self.type.upper()]


@dataclass
class Star:
    ra: float
    dec: float
    proper: str
    mag: float
    constellation: str
    hipparcos: int

    @property
    def ra_deg(self) -> float:
        return (self.ra - 24 if self.ra > 12 else self.ra) * 15

    def __hash__(self):
        return f"{self.hipparcos}{self.ra}{self.dec}"

    def __str__(self):
        return self.proper or f"hip{self.hipparcos}"


@dataclass
class Point:
    ra: float
    dec: float

    @property
    def ra_deg(self) -> float:
        return (self.ra - 24 if self.ra > 12 else self.ra) * 15


@dataclass
class Line:
    thin: bool
    segment: List[Star]


class Constellation:
    def __init__(self, constellation, client: "AstronomyClient"):
        self.iau: str = constellation["iau"]
        self.english_name: str = constellation["common_name"]["english"]
        self.native_name: str = constellation["common_name"]["native"]
        self.lines: List[Line] = []
        self.__parent_client = client
        for line in constellation["lines"]:
            if line[0] == "thin":
                thin = True
                line.pop(0)
            else:
                thin = False
            self.lines.append(
                Line(thin, [client.hipparcos(star) for star in line])
            )

    @property
    def orthographic_image(self) -> str:
        return f"https://raw.githubusercontent.com/crazygmr101/Almanac/master/assets/orbs/{self.iau}.png"

    @property
    def hammer_image(self) -> str:
        return f"https://raw.githubusercontent.com/crazygmr101/Almanac/master/assets/hammer/{self.iau}.png"

    @cached_property
    def main_stars(self) -> Set[Star]:
        return set(itertools.chain(*[part.segment for part in self.lines]))

    @cached_property
    def main_star_count(self) -> int:
        return len(self.main_stars)

    @cached_property
    def named_stars(self) -> Iterable[Star]:
        return filter(lambda star: star.proper, self)

    def __iter__(self) -> Iterable[Star]:
        for star in self.__parent_client.stars:
            if (
                star.constellation
                and star.constellation.lower() == self.iau.lower()
            ):
                yield star

    @cached_property
    def bounds(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        max_ra = self.lines[0].segment[0].ra
        min_ra = self.lines[0].segment[0].ra
        max_dec = self.lines[0].segment[0].dec
        min_dec = self.lines[0].segment[0].dec
        for line in self.lines:
            for star in line.segment:
                max_ra = max(max_ra, star.ra)
                min_ra = min(min_ra, star.ra)
                max_dec = max(max_dec, star.dec)
                min_dec = min(min_dec, star.dec)
        return (min_ra, max_ra), (min_dec, max_dec)

    @cached_property
    def center(self) -> Point:
        ra, dec = self.bounds
        return Point((ra[0] + ra[1]) / 2, (dec[0] + dec[1]) / 2)
