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
from calendar import TextCalendar
from datetime import datetime

from discord.ext import commands

from bot import Almanac, AlmanacContext, AlmanacCommand
from module_services.calendar import CalendarView, CalendarService


class CalendarModule(commands.Cog, CalendarService):
    def __init__(self, bot: Almanac):
        self.bot = bot

    @property
    def description(self) -> str:
        return "Your virtual calendar"

    @commands.command(
        cls=AlmanacCommand,
        brief="Interactive calendar",
        usage="`;calendar` - show the current month\n"
              "`;calendar 2020` - start at 2020, with the same month as now\n"
              "`;calendar mar 2020` - start on march 2020",
        arg_list={"time": [True, str, "Month/year to start the calendar at"]}
    )
    async def calendar(self, ctx: AlmanacContext, *, time: str = None):
        if not time:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year, month = self.parse_ym(time)
        cal = TextCalendar()
        await ctx.send(f"```"
                       f"{cal.formatmonth(year, month, 3)}"
                       f"```",
                       view=CalendarView(cal, year, month))


def setup(bot: Almanac):
    bot.add_cog(CalendarModule(bot))
