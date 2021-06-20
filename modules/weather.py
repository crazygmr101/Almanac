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

from discord import Embed
from discord.ext import commands

from bot import Almanac, AlmanacContext
from module_services import WeatherService


class WeatherModule(commands.Cog, WeatherService):
    @commands.command(
        brief="Show the current conditions for a city"
    )
    async def weather(self, ctx: AlmanacContext, *, city: str):
        await ctx.send(embed=await self.current_conditions(city))

    @commands.group(
        brief="NWS lookups"
    )
    async def nws(self, ctx: commands.Context):
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
        brief="Lookup point data for a lat/long"
    )
    async def point(self, ctx: commands.Context, lat: int, long: int):
        await ctx.send(embed=await self.point_data(lat, long))

    def __init__(self, bot: Almanac):
        super(WeatherModule, self).__init__()
        self.bot = bot

    @property
    def description(self) -> str:
        return "Weather commands"



def setup(bot: Almanac):
    bot.add_cog(WeatherModule(bot))
