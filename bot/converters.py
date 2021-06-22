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
from discord.ext.commands import CommandError

from bot import AlmanacContext


class MapLayerType:
    TYPES = {
        "clouds": ["cloud", "cloudcover"],
        "precipitation": ["precipitation", "precip"],
        "pressure": ["psi", "pressure"],
        "wind": ["windspeed", "wind"],
        "temperature": ["heat", "temp", "temperature"]
    }

    def __init__(self, layer_type: str):
        self.layer_type = layer_type

    def __str__(self):
        return f"{self.layer_type}_new"

    @classmethod
    async def convert(cls, ctx: AlmanacContext, argument: str):
        argument = argument.lower()
        for typ, aliases in cls.TYPES.items():
            if argument in aliases:
                return cls(typ)
        raise CommandError(f"`{argument}` is an invalid map layer. Valid layers are {', '.join(TYPES.keys())} ")
