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
from datetime import datetime

import tanjun

from bot.converters import parse_datetime
from libs.astronomy import AstronomyAPI
from module_services.bot import EmbedCreator

component = tanjun.Component()
astro_group = component.with_slash_command(
    tanjun.SlashCommandGroup("astro", "Astronomy commands")
)


@astro_group.with_command
@tanjun.with_int_slash_option("year", "The year to look up")
@tanjun.as_slash_command("seasons", "Season Times")
async def seasons(
    ctx: tanjun.SlashContext,
    year: int,
    _api: AstronomyAPI = tanjun.injected(type=AstronomyAPI),
    _bot: EmbedCreator = tanjun.injected(type=EmbedCreator),
):
    await ctx.respond(
        embed=_bot.ok_embed(
            title=f"Seasons for {year}",
            description="\n".join(
                f"**{season}**: {time}"
                for season, time in zip(
                    [
                        "March Equinox",
                        "June Solstice",
                        "September Equinox",
                        "December Solstice",
                    ],
                    _api.seasons(year).formatted_times,
                )
            ),
        )
    )


@astro_group.with_command
@tanjun.with_str_slash_option(
    "date", "The date to look up", converters=(parse_datetime,)
)
@tanjun.as_slash_command("date", "Data about the date")
async def date_data(
    ctx: tanjun.SlashContext,
    date: datetime,
    _api: AstronomyAPI = tanjun.injected(type=AstronomyAPI),
    _bot: EmbedCreator = tanjun.injected(type=EmbedCreator),
):
    await ctx.respond(
        embed=_bot.ok_embed(
            title=f"Data for {date.strftime('%b %d %Y')}",
            description=f"**Moon**: {_api.moon_phase(date.year, date.month, date.day)}",
        )
    )


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
