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
import discord
from discord.ext import commands

from bot import AlmanacContext, AlmanacCommand
from module_services.bot import EmbedCreator


class HelpService(EmbedCreator):
    def __init__(self):
        super(HelpService, self).__init__()

    async def get_command_list(self, ctx: AlmanacContext) -> discord.Embed:
        return self.ok_embed(
            title="Command list",
            description="\n".join(
                [
                    f"`{command.qualified_name}` - {command.brief}"
                    for command in ctx.bot.walk_commands()
                    if not isinstance(command, commands.Group)
                    and command.qualified_name != "help"
                ]
            ),
        ).set_footer(text="Do ;help command for help with a command")

    async def get_help_for_command(
        self, ctx: AlmanacContext, command: str
    ) -> discord.Embed:
        cmd: AlmanacCommand
        for cmd in ctx.bot.walk_commands():
            if cmd.qualified_name.lower() == command:
                break
        else:
            return self.error_embed(
                title="Command not found",
                description=f"`{command}` is an invalid command. Do `;help commands` to view a list of commands",
            )
        if isinstance(cmd, commands.Group):
            return self.ok_embed(
                title=f"`;{cmd.qualified_name}`",
                description=cmd.brief,
            ).add_field(
                name="Subcommands",
                value="\n".join(
                    f"`{subcommand.qualified_name}` - {subcommand.brief}"
                    for subcommand in cmd.walk_commands()
                ),
            )
        else:
            print(cmd.signature)
            embed = self.ok_embed(
                title=f"`;{cmd.qualified_name} {cmd.signature}`",
                description=cmd.brief,
            ).add_field(name="Usage Examples", value=cmd.usage, inline=False)
            if cmd.arg_list:
                embed.add_field(
                    name="Argument List",
                    value="\n".join(cmd.argument_doc),
                    inline=False,
                )
            return embed
