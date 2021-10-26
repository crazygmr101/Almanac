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
from typing import Any, Dict, Iterable, Tuple


class DatabaseProto:
    def set_setting(self, user: int, setting: str, value: Any):
        raise NotImplementedError

    def get_setting(self, user: int, setting: str) -> Any:
        raise NotImplementedError

    def get_settings(self, user: int) -> "UserSettings":
        raise NotImplementedError


class InvalidSetting(Exception):
    ...


class UserSettings:
    def __init__(self, user: int, imperial: bool):
        self.user = user
        self.imperial = imperial
        self.__current = 0
        self.__elements = [self.user, self.imperial]

    def values(self) -> Dict[str, Any]:
        return {"Unit System": "Imperial" if self.imperial else "Metric"}
