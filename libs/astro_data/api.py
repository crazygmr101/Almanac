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
from math import pi
from typing import TextIO, Optional

import pandas as pd

from libs.astro_data.models import DSO, Star, Constellation


class AstronomyClient:
    def __init__(
        self, dso_fp: TextIO, ngc_fp: TextIO, hyg_fp: TextIO, con_fp: TextIO
    ):
        self.dsos = [
            DSO(line)
            for line in dso_fp.readlines()
            if (line and not line.startswith("#"))
        ]

        pdata = pd.read_csv(hyg_fp)

        self.stars = [
            Star(
                line.ra * 180 / pi,
                line.dec * 180 / pi,
                line.proper if isinstance(line.proper, str) else None,
                line.mag,
                line.con if isinstance(line.con, str) else None,
                line.hip,
            )
            for line in pdata.itertuples()
            if line.id != 0
        ]

        self._hipparcos_mapping = {star.hipparcos: star for star in self.stars}

        self.constellations = [
            Constellation(constellation, self)
            for constellation in json.load(con_fp)["constellations"]
        ]

        # parse openngc dataset
        dataset = {
            line.split(";")[0]: line.split(";")[1:]
            for line in ngc_fp.readlines()[1:]
        }

        for dso in self.dsos:
            if line := dataset.get(f"NGC{dso.ngc:>04}", None):
                dso.common_names = line[-3].strip('"')
                dso.ned_notes = line[-2].strip('"')
                dso.open_ngc_notes = line[-1].strip('"')
                dso.constellation = line[3]
            elif line := dataset.get(f"IC{dso.ngc:>04}", None):
                dso.common_names = line[-3].strip('"')
                dso.ned_notes = line[-2].strip('"')
                dso.open_ngc_notes = line[-1].strip('"')
                dso.constellation = line[3]

    def m(self, number: int) -> Optional[DSO]:
        for dso in self.dsos:
            if dso.m == number:
                return dso
        else:
            return None

    def ngc(self, number: int) -> Optional[DSO]:
        for dso in self.dsos:
            if dso.ngc == number:
                return dso
        else:
            return None

    def hipparcos(self, number: int) -> Optional[Star]:
        return self._hipparcos_mapping.get(number, None)

    def constellation(self, iau: str) -> Optional[Constellation]:
        for constellation in self.constellations:
            if constellation.iau.lower() == iau.lower():
                return constellation
        else:
            return None
