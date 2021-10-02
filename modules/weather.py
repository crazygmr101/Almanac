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

import tanjun

from bot.proto import WeatherServiceProto, DatabaseProto

component = tanjun.Component()
weather_group = component.with_slash_command(tanjun.SlashCommandGroup("weather", "Weather commands"))
weather_nws_group = weather_group.with_command(tanjun.SlashCommandGroup("nws", "Get MWS data"))


@weather_group.with_command
@tanjun.with_str_slash_option("location", "Location to look up")
@tanjun.as_slash_command("current", "Current weather at a location")
async def current(ctx: tanjun.SlashContext, location: str,
                  _service: WeatherServiceProto = tanjun.injected(type=WeatherServiceProto),
                  _db: DatabaseProto = tanjun.injected(type=DatabaseProto)):
    await ctx.respond(embed=await _service.current_conditions(location, _db.get_settings(ctx.author.id)))


@weather_nws_group.with_command
@tanjun.with_float_slash_option("latitude", "Latitude of the location")
@tanjun.with_float_slash_option("longitude", "Longitude of the location")
@tanjun.as_slash_command("point", "Lookup NWS point data for a lat/long")
async def point(ctx: tanjun.SlashContext, latitude: float, longitude: float,
                _service: WeatherServiceProto = tanjun.injected(type=WeatherServiceProto)):
    await ctx.respond(embed=await _service.point_data(latitude, longitude))


@weather_group.with_command
@tanjun.with_int_slash_option("zoom", "Zoom level", choices=[(f"Level {n}", n) for n in range(1, 17)], default=8)
@tanjun.with_str_slash_option("layer", "Map type to look up", default="clouds",
                              choices=[(typ.title(), typ) for typ in WeatherServiceProto.MAP_TYPES])
@tanjun.with_str_slash_option("location", "Location to look up")
@tanjun.as_slash_command("weather-map", "Look up the weather map for a location", sort_options=True)
async def weather_map(ctx: tanjun.SlashContext, zoom: int, layer: str, location: str,
                      _service: WeatherServiceProto = tanjun.injected(type=WeatherServiceProto)):
    await ctx.respond(embed=await _service.weather_map(location, zoom, layer))


@weather_group.with_command
@tanjun.with_str_slash_option("location", "Location to look up")
@tanjun.as_slash_command("radar", "Look up the radar for a location")
async def radar(ctx: tanjun.SlashContext, location: str,
                _service: WeatherServiceProto = tanjun.injected(type=WeatherServiceProto)):
    await ctx.respond(embed=await _service.radar_map(location))


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
