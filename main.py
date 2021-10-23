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
import asyncio
import logging
import os
from pathlib import Path

import dotenv

from bot import LoggingHandler
from libs.astronomy import AstronomyAPI
from libs.nasa import NasaAPI
from module_services.geocoding import Geocoder

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
if os.getenv("CUSTOM_LOGGER") == "1":
    logging.setLoggerClass(LoggingHandler)

import hikari  # noqa E402
import tanjun  # noqa E402
from bot.proto import DatabaseProto  # noqa 402
from bot.impl import DatabaseImpl  # noqa E402
from module_services.bot import BotUtils  # noqa E402
from module_services.weather import WeatherAPI  # noqa E402

db = DatabaseImpl.connect()

bot = hikari.GatewayBot(token=os.getenv("TOKEN"))
client = (
    tanjun.Client.from_gateway_bot(
        bot,
        declare_global_commands=int(os.getenv("GUILD"))
        if os.getenv("GUILD")
        else True,
    )  # noqa E131
    .set_type_dependency(WeatherAPI, WeatherAPI())
    .set_type_dependency(DatabaseProto, db)
    .set_type_dependency(AstronomyAPI, AstronomyAPI())
    .set_type_dependency(Geocoder, Geocoder())
    .set_type_dependency(NasaAPI, NasaAPI())
    .set_type_dependency(BotUtils, BotUtils())
    .set_auto_defer_after(0.1)
    .load_modules(*Path("./modules").glob("**/*.py"))
)


async def clear_commands():
    async with hikari.RESTApp().acquire(
        os.getenv("TOKEN"), token_type="Bot"
    ) as rest:
        async with tanjun.Client(rest) as rest_client:
            await rest_client.clear_commands()


if os.getenv("CLEAR"):
    asyncio.run(clear_commands())

bot.run()
