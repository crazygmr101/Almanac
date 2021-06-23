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
from typing import Optional

from discord.ext import commands

from bot import Almanac, AlmanacContext, AlmanacCommand
from bot.converters import MapLayerType
from module_services import WeatherService


class WeatherModule(commands.Cog, WeatherService):

    def __init__(self, bot: Almanac):
        super(WeatherModule, self).__init__()
        self.bot = bot

    @property
    def description(self) -> str:
        return "Weather commands"

    @commands.group(
        brief="Weather lookups"
    )
    async def weather(self, ctx: AlmanacContext):
        if not ctx.subcommand_passed:
            await ctx.send(embed=self.error_embed(
                title="Must pass a subcommand",
                description="\n".join(
                    f"`nws {cmd.name}` - {cmd.brief}"
                    for cmd in self.weather.walk_commands()
                    if isinstance(cmd, commands.Command)
                )
            ))

    @weather.command(
        cls=AlmanacCommand,
        brief="Show the current conditions for a city",
        arg_list={
            "location": [False, str, "Location to look up"]
        }
    )
    async def current(self, ctx: AlmanacContext, *, location: str):
        await ctx.send(embed=await self.current_conditions(location))

    @commands.group(
        brief="NWS lookups"
    )
    async def nws(self, ctx: AlmanacContext):
        if not ctx.subcommand_passed:
            await ctx.send(embed=self.error_embed(
                title="Must pass a subcommand",
                description="\n".join(
                    f"`nws {cmd.name}` - {cmd.brief}"
                    for cmd in self.nws.walk_commands()
                    if isinstance(cmd, commands.Command)
                )
            ))

    @nws.command(
        cls=AlmanacCommand,
        brief="Lookup NWS point data for a lat/long",
        arg_list={
            "lat": [False, float, "Latitude of the location"],
            "long": [False, float, "Longitude of the location"]
        }
    )
    async def point(self, ctx: AlmanacContext, lat: float, long: float):
        await ctx.send(embed=await self.point_data(lat, long))

    @weather.command(
        cls=AlmanacCommand,
        brief="Look up a weather map for a city",
        usage="`;map new york city, ny` - Look up a clouds map at zoom level 8\n"
              "`;map 7 new york city` - Look up a clouds map at zoom level 7\n"
              "`;map precip new york city` - Look up a precipitation map at default zoom",
        arg_list={
            "zoom": [True, int, "Zoom level from 1 to 16 - defaults to 8"],
            "layer_type": [True, MapLayerType, "Map type: " + ", ".join(MapLayerType.TYPES) + "defaults to clouds"],
            "location": [False, str, "Location to look up"]
        }
    )
    async def map(self, ctx: AlmanacContext, zoom: Optional[int], layer_type: Optional[MapLayerType], *, location: str):
        layer_type = layer_type.layer_type if layer_type else "clouds"
        zoom = zoom or 8
        await ctx.send(file=await self.weather_map(location, zoom, layer_type))

    @weather.command(
        cls=AlmanacCommand,
        brief="Look up the local radar image for a city",
        arg_list={
            "location": [False, str, "Location to look up"]
        }
    )
    async def radar(self, ctx: AlmanacContext, *, location: str):
        await ctx.send(embed=await self.radar_map(location))


def setup(bot: Almanac):
    bot.add_cog(WeatherModule(bot))
