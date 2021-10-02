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

from bot.proto import DatabaseProto

component = tanjun.Component()
settings_group = component.with_slash_command(tanjun.SlashCommandGroup("settings", "Settings"))


@settings_group.with_command
@tanjun.with_str_slash_option("value", "The value to set it to")
@tanjun.with_str_slash_option("setting", "The setting to set",
                              choices=[(choice[1][3], choice[0]) for choice in DatabaseProto.VALID_SETTINGS.items()])
@tanjun.as_slash_command("set", "Set config option")
async def set_setting(ctx: tanjun.SlashContext, setting: str, value: str,
                      _db: DatabaseProto = tanjun.injected(type=DatabaseProto)):
    try:
        _db.set_setting(ctx.author.id, setting, value)
        await ctx.respond(
            content=None,
            embed=_db.ok_embed("Setting changed",
                               f"Set {DatabaseProto.VALID_SETTINGS[setting][3].lower()} to `{value}`"))
    except ValueError as err:
        await ctx.respond(
            content=None,
            embed=_db.error_embed("Invalid value", str(err)))


@settings_group.with_command
@tanjun.as_slash_command("list", "List settings")
async def list_settings(ctx: tanjun.SlashContext, _db: DatabaseProto = tanjun.injected(type=DatabaseProto)):
    await ctx.respond(
        content=None,
        embed=_db.ok_embed(
            "Settings list",
            "\n".join(f"**{name}** - {value}" for name, value in _db.get_settings(ctx.author.id))
        )
    )


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
