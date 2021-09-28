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
from discord.ext import commands

from bot import AlmanacContext, Almanac, AlmanacCommand
from module_services import HelpService


class HelpModule(commands.Cog, HelpService):
    def __init__(self, bot: Almanac):
        super(HelpModule, self).__init__()
        self.bot = bot

    @commands.group()
    async def help(self, ctx: AlmanacContext):
        if ctx.invoked_subcommand:
            return
        command = " ".join(ctx.message.content.split(" ")[1:])
        if not command.strip():
            await ctx.send(embed=await self.get_command_list(ctx))
        else:
            await ctx.send(embed=await self.get_help_for_command(ctx, command))

    @help.command(
        cls=AlmanacCommand,
        brief="Show the command list",
        usage="`;help commands`",
        arg_list={}
    )
    async def commands(self, ctx: AlmanacContext):
        await ctx.send(embed=await self.get_command_list(ctx))


def setup(bot: Almanac):
    bot.add_cog(HelpModule(bot))
