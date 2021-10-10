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
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, cast


@dataclass(frozen=True)
class SeasonTimes:
    vernal_equinox: datetime
    summer_solstice: datetime
    autumnal_equinox: datetime
    winter_solstice: datetime

    @property
    def times(self) -> Tuple[datetime, datetime, datetime, datetime]:
        return (
            self.vernal_equinox,
            self.summer_solstice,
            self.autumnal_equinox,
            self.winter_solstice,
        )

    @property
    def formatted_times(self) -> Tuple[str, str, str, str]:
        return cast(  # typing is a scam :(
            Tuple[str, str, str, str],
            tuple(time.strftime("%b %d  %H:%M") for time in self.times),
        )


@dataclass(frozen=True)
class MoonPhase:
    degrees: float

    @property
    def emoji(self) -> str:
        return "🌑🌘🌗🌖🌕🌔🌓🌒"[round(self.degrees / 45) % 8]

    @property
    def name(self) -> str:
        return [
            "New Moon",
            "Waxing Crescent",
            "First Quarter",
            "Waxing Gibbous",
            "Full Moon",
            "Waning Gibbous",
            "Third Quarter",
            "Waning Crescent",
        ][round(self.degrees / 45) % 8]

    def __str__(self) -> str:
        return f"{self.emoji} {self.name} ({self.degrees:.1f}°)"
