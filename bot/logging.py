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

import logging

from colorama import init, Fore, Style

init()

colors = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": f"{Fore.LIGHTWHITE_EX}",
    "INFO": "",
    "WARNING": f"{Fore.YELLOW}{Style.BRIGHT}",
    "ERROR": f"{Fore.LIGHTRED_EX}{Style.BRIGHT}",
    "CRITICAL": f"{Fore.RED}{Style.BRIGHT}",
}
colors2 = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": Fore.LIGHTWHITE_EX,
    "INFO": Fore.BLUE,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.LIGHTRED_EX,
    "CRITICAL": Fore.RED,
}
styles = {
    "TRACE": f"{Fore.WHITE}{Style.DIM}",
    "DEBUG": f"{Fore.LIGHTWHITE_EX}",
    "INFO": "",
    "WARNING": "",
    "ERROR": "",
    "CRITICAL": Style.BRIGHT,
}
names = {
    "bot": Fore.BLUE,
    "discord.client": Fore.GREEN,
    "discord.gateway": Fore.MAGENTA,
    "discord.ext.commands.core": Fore.YELLOW,
    "discord.http": Fore.RED
}


class LoggingHandler(logging.StreamHandler):

    def emit(self, record: logging.LogRecord) -> None:
        name = record.name
        level = record.levelno  # noqa F841
        level_name = record.levelname
        if name == "bot":
            split = record.msg.split(":")
            if len(split) == 1:
                sub = None
                message = split[0]
            else:
                sub = split[0]
                message = ":".join(split[1:])
        else:
            message = record.msg
            sub = None

        message %= record.args

        print(f"{colors2[level_name]}{styles[level_name]}{level_name:>8}{Style.RESET_ALL}"
              f" "
              f"{Style.BRIGHT}{names[name]}{name}{Style.RESET_ALL} " +
              (f"» {Style.BRIGHT}{Fore.LIGHTBLUE_EX}{sub}{Style.RESET_ALL} " if sub else '') +
              f"» "
              f"{colors[level_name]}{message}{Style.RESET_ALL}")
