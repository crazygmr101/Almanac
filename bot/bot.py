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

from __future__ import annotations

import asyncio
import logging
import os
from typing import TYPE_CHECKING, Dict, Tuple

import aiohttp
import discord
import dotenv
from discord.ext import tasks, commands
from discord.ext.commands import MinimalHelpCommand

from libs.openweathermap import OpenWeatherMapAPI

if TYPE_CHECKING:
    from bot import AlmanacContext

import bot


class Almanac(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super(Almanac, self).__init__(*args, help_command=None, command_prefix=";", **kwargs)
        dotenv.load_dotenv()
        self.shutting_down = False
        self.TRACE = 7
        for logger in [
            "bot",
            "discord.client",
            "discord.gateway",
            "discord.http",
            "discord.ext.commands.core"
        ]:
            logging.getLogger(logger).setLevel(logging.DEBUG if logger == "bot" else logging.INFO)
            logging.getLogger(logger).addHandler(bot.LoggingHandler())
        self.logger = logging.getLogger("bot")

        async def on_ready():
            self.logger.info(f"Almanac online!")
            await self.change_presence(activity=discord.Game(f";help | {len(self.guilds)} servers"))
            self.status_loop.start()

        self.add_listener(on_ready, "on_ready")

    def load_modules(self) -> None:
        modules = [
            "calendar",
            "weather",
            "help"
        ]
        for module in modules:
            self.logger.info(f"cogs:Loading {module}")
            self.load_extension(f"modules.{module}")

    @tasks.loop(minutes=20)
    async def status_loop(self):
        await self.change_presence(activity=discord.Game(f";help | {len(self.guilds)} servers"))

    async def on_message(self, message: discord.Message):

        if not message.guild:
            return

        ctx: bot.AlmanacContext = await self.get_context(message, cls=bot.AlmanacContext)
        await self.invoke(ctx)

    async def start(self, *args, **kwargs):  # noqa: C901
        """|coro|
        A shorthand coroutine for :meth:`login` + :meth:`connect`.
        Raises
        -------
        TypeError
            An unexpected keyword argument was received.
        """
        reconnect = kwargs.pop('reconnect', True)

        if kwargs:
            raise TypeError("unexpected keyword argument(s) %s" % list(kwargs.keys()))

        for i in range(0, 6):
            try:
                self.logger.debug(f"bot:Connecting, try {i + 1}/6")
                await self.login(os.getenv("TOKEN"))
                break
            except aiohttp.ClientConnectionError as e:
                self.logger.warning(f"bot:Connection {i + 1}/6 failed")
                self.logger.warning(f"bot:  {e}")
                self.logger.warning(f"bot:Waiting {2 ** (i + 1)} seconds")
                await asyncio.sleep(2 ** (i + 1))
                self.logger.info("bot:Attempting to reconnect")
        else:
            self.logger.critical("bot:Failed after 6 attempts")
            return

        for cog in self.cogs:
            cog = self.get_cog(cog)
            if not cog.description and cog.qualified_name:
                self.logger.critical(f"cogs:Cog {cog.qualified_name} has no description")
                return

        missing_brief = []
        for command in self.commands:
            if not command.brief and command.name != "help":
                missing_brief.append(command)

        if missing_brief:
            self.logger.error("cmds:The following commands are missing help text")
            for i in missing_brief:
                self.logger.error(f"cmds: - {i.cog.qualified_name}.{i.name}")
            return

        await self.connect(reconnect=reconnect)
