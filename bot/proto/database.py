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
import typing
from dataclasses import dataclass

from module_services.bot import BotService


class DatabaseProto(BotService):
    def set_setting(self, user: int, setting: str, value: typing.Any):
        raise NotImplementedError

    def get_setting(self, user: int, setting: str) -> typing.Any:
        raise NotImplementedError

    def get_settings(self, user: int) -> "UserSettings":
        raise NotImplementedError


class InvalidSetting(Exception):
    ...


@dataclass(frozen=True)
class UserSettings:
    user: int
    imperial: bool

    def values(self) -> typing.Dict[str, typing.Any]:
        return {
            "Unit System": "Imperial" if self.imperial else "Metric"
        }

    def __iter__(self) -> typing.Iterable[typing.Tuple[str, typing.Any]]:
        for name, value in self.values().items():
            yield name, value
