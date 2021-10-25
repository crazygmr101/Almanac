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
from skyfield.errors import EphemerisRangeError

from bot.converters import parse_datetime
from libs.astro_data import AstronomyClient
from libs.astronomy import AstronomyEventAPI
from libs.helpers import ra_to_str, dd_to_str_dms
from libs.nasa import NasaAPI, APOD
from module_services.bot import BotUtils

component = tanjun.Component()
astro_group = component.with_slash_command(
    tanjun.SlashCommandGroup("astro", "Astronomy commands")
)
astro_constellation_group = astro_group.with_command(
    tanjun.SlashCommandGroup("constellations", "Constellation commands")
)
hooks = tanjun.SlashHooks()


@hooks.with_on_error
async def on_error(ctx: tanjun.SlashContext, error: Exception) -> bool:
    ctx.set_ephemeral_default(True)
    if isinstance(error, EphemerisRangeError):
        await ctx.respond(
            f"Almanac only supports dates from {AstronomyEventAPI.year_range[0]} to {AstronomyEventAPI.year_range[1]}"
        )
    return True


@hooks.add_to_command
@astro_group.with_command
@tanjun.with_int_slash_option("year", "The year to look up")
@tanjun.as_slash_command("seasons", "Season Times")
async def seasons(
    ctx: tanjun.SlashContext,
    year: int,
    _api: AstronomyEventAPI = tanjun.injected(type=AstronomyEventAPI),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
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


@hooks.add_to_command
@astro_group.with_command
@tanjun.with_str_slash_option(
    "date", "The date to look up", converters=(parse_datetime,), default=None
)
@tanjun.as_slash_command("apod", "Astronomy Picture of the Day")
async def date_data(
    ctx: tanjun.SlashContext,
    date: datetime,
    _api: NasaAPI = tanjun.injected(type=NasaAPI),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
):
    date = date or datetime.now()
    apod: APOD = await _api.apod(date)
    response_embed = _bot.ok_embed(
        title=f"APOD for {date.strftime('%b %d %Y')}",
        description=f"**{apod.title}**\n" f"{apod.explanation}",
    )
    if apod.media_type == "video":
        response_embed.add_field("Video URL", apod.url)
    else:
        response_embed.set_image(apod.url)
    await ctx.respond(embed=response_embed)


@hooks.add_to_command
@astro_group.with_command
@tanjun.with_str_slash_option(
    "date", "The date to look up", converters=(parse_datetime,)
)
@tanjun.as_slash_command("date", "Data about the date")
async def date_data(
    ctx: tanjun.SlashContext,
    date: datetime,
    _api: AstronomyEventAPI = tanjun.injected(type=AstronomyEventAPI),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
):
    await ctx.respond(
        embed=_bot.ok_embed(
            title=f"Data for {date.strftime('%b %d %Y')}",
            description=f"**Moon**: {_api.moon_phase(date.year, date.month, date.day)}",
        )
    )


@astro_constellation_group.with_command
@tanjun.with_str_slash_option(
    "type",
    "Type of map to view",
    choices={
        "Orb": "orthographic",
        "Locator": "hammer",
    },
    default="orthographic",
)
@tanjun.with_str_slash_option("constellation", "Constellation to view")
@tanjun.as_slash_command("view", "View an map of a constellation")
async def constellation_orthographic(
    ctx: tanjun.SlashContext,
    constellation: str,
    type: str,
    _dso: AstronomyClient = tanjun.injected(type=AstronomyClient),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
):
    const = _dso.constellation(constellation)
    if type == "orthographic":
        desc = f"**{const.english_name}**\n"
        if const.named_stars:
            desc += "**Named Stars**: " + ", ".join(
                star.proper for star in const.named_stars
            )
    else:
        desc = (
            f"**RA**: {ra_to_str(const.center.ra)}\n"
            f"**Dec**: {dd_to_str_dms(const.center.dec)}"
        )
    await ctx.respond(
        _bot.ok_embed(
            title=f"{const.native_name} `{const.iau}`", description=desc
        ).set_image(
            const.orthographic_image
            if type == "orthographic"
            else const.hammer_image
        )
    )


@astro_constellation_group.with_command
@tanjun.as_slash_command("list", "List all 88 constellations")
async def constellation_list(
    ctx: tanjun.SlashContext,
    _dso: AstronomyClient = tanjun.injected(type=AstronomyClient),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
):
    ctx.set_ephemeral_default(True)
    await ctx.respond(
        _bot.ok_embed(
            title="Constellation List",
            description="\n".join(
                f"`{constellation.iau}` - {constellation.native_name} - "
                f"{constellation.english_name}"
                for constellation in _dso.constellations
            ),
        )
    )


@astro_group.with_command
@tanjun.with_int_slash_option("number", "The number to look up")
@tanjun.with_str_slash_option(
    "catalog",
    "The type of object to look up",
    choices={"Messier": "m", "NGC": "ngc"},
)
@tanjun.as_slash_command("lookup-object", "Look up a Messier or NGC object")
async def lookup_object(
    ctx: tanjun.SlashContext,
    catalog: str,
    number: int,
    _dso: AstronomyClient = tanjun.injected(type=AstronomyClient),
    _bot: BotUtils = tanjun.injected(type=BotUtils),
):
    obj = _dso.ngc(number) if catalog == "ngc" else _dso.m(number)
    if obj:
        other_catalog_id = obj.m if catalog == "ngc" else obj.ngc
        other_catalog_str = (
            f"Also known as **{'M' if catalog == 'ngc' else 'NGC'}{other_catalog_id:>04}**\n"
            if other_catalog_id
            else ""
        )
        await ctx.respond(
            embed=_bot.ok_embed(
                title=f"{catalog.upper()}{number:>04}",
                description=f"**Common Name**: {obj.common_names or '-'}\n"
                f"**Type**: {obj.pretty_type}\n"
                f"**Constellation**: {obj.constellation}\n"
                f"**Location**: {obj.location}\n"
                f"**Magnitude**: {obj.magnitude}\n"
                f"{other_catalog_str}",
            )
        )
    else:
        await ctx.respond(f"Object not found in {catalog.upper()} catalog")


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
