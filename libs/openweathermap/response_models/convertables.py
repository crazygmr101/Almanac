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
from bot.proto.database import UserSettings
from libs.openweathermap.helpers import cloud_coverage_label, direction_for


class Temperature(float):
    def convert(self, settings: UserSettings) -> "Temperature":
        return self if settings.imperial else (self - 32) / 1.8

    def formatted(self, settings: UserSettings) -> str:
        converted = self.convert(settings)
        return f"{int(converted)}°{'F' if settings.imperial else 'C'}"


class Speed(float):
    def convert(self, settings: UserSettings) -> "Speed":
        return self if settings.imperial else self * 1.60934

    def formatted(self, settings: UserSettings) -> str:
        converted = self.convert(settings)
        return f"{int(converted)} {'mph' if settings.imperial else 'km/h'}"


class Distance(float):
    def convert(self, settings: UserSettings) -> "Distance":
        return self if settings.imperial else self * 1.60934

    def formatted(self, settings: UserSettings) -> str:
        converted = self.convert(settings)
        return f"{int(converted)} {'mi' if settings.imperial else 'km'}"


class Clouds:
    def __init__(self, level: int):
        self._level = level

    def __str__(self) -> str:
        return cloud_coverage_label(self._level)

    @property
    def emoji(self) -> str:
        return "☁️" if self._level > 65 else "🌥" if self._level > 40 else "☀️"


class Wind:
    def __init__(self, direction: int, speed: Speed):
        self._dir = direction
        self._speed = speed

    def convert(self, settings: UserSettings) -> "Wind":
        return self.__class__(self._dir, self._speed.convert(settings))

    def formatted(self, settings: UserSettings) -> str:
        return f"{self._speed.formatted(settings)} {direction_for(self._dir)}"


class Precipitation(float):
    def convert(self, settings: UserSettings) -> "Precipitation":
        return self / 25.4 if settings.imperial else self

    def formatted(self, settings: UserSettings) -> str:
        if settings.imperial:
            return f"{self.convert(settings):.2f} in"
        else:
            return f"{self.convert(settings):.0f} mm"

    def formatted_or(
        self, settings: UserSettings, default: str = "", fmt: str = "%s"
    ) -> str:
        return fmt % self.formatted(settings) if self > 0 else default
