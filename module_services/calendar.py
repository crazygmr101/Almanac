import re
from calendar import TextCalendar
from datetime import datetime
from typing import Tuple, Optional

from discord import Interaction, Message, ButtonStyle
from discord.ui import View, button, Button

MONTHS = "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"


class CalendarService:

    def parse_ym(self, time: str) -> Tuple[int, int]:
        now = datetime.now()
        time = re.sub(r"\s(ad|bc)", "$1", time.lower())
        split = re.split(r"[- /]", time)
        if len(split) == 1:
            token = split[0]
            if month := self.try_parse_month(token) is not None:
                return now.year, month
        if len(split) > 2:
            return now.year, now.month
        month, year = self.try_parse_month(split[0]), self.try_parse_year(split[1])
        if month is not None and year is not None:
            return year, month
        if month is not None:
            possible_m_y = True, month
        else:
            possible_m_y = False, 0
        month, year = self.try_parse_month(split[1]), self.try_parse_year(split[0])
        if month is not None and year is not None:
            return year, month
        if year is not None:
            possible_y_m = True, year
        else:
            possible_y_m = False, 0
        if possible_m_y[0]:
            return now.year, possible_m_y[1]
        if possible_y_m[0]:
            return possible_y_m[1], now.month
        return now.year, now.month

    def try_parse_year(self, year: str) -> Optional[int]:
        year = year.lower().replace(".", "")
        if year.endswith("bc") or year.endswith("ad"):
            year = year[:-2]
            era = -1 if year.endswith("bc") else 1
        else:
            era = 1
        try:
            year = era * int(year)
        except ValueError:
            return None
        return year

    def try_parse_month(self, month: str) -> Optional[int]:
        # see if it's a text month
        if month.lower()[:3] in MONTHS:
            return MONTHS.index(month.lower()[:3]) + 1
        # see if it's a number month
        try:
            token = int(month)
        except ValueError:
            # it's not a number month or a 3 letter month, return now
            return None
        if 1 <= token <= 12:
            return token
        return None


class CalendarView(View):
    def __init__(self, calendar: TextCalendar, year: int, month: int):
        super(CalendarView, self).__init__()
        self.year = year
        self.month = month
        self.calendar = calendar

    @button(label="← Year")
    async def prev_year(self, btn: Button, interaction: Interaction):
        msg: Message = interaction.message
        self.year -= 1
        await self._refresh(msg)

    @button(label="← Month")
    async def prev_month(self, btn: Button, interaction: Interaction):
        msg: Message = interaction.message
        self.month -= 1
        await self._refresh(msg)

    @button(label="Today", style=ButtonStyle.primary)
    async def today(self, btn: Button, interaction: Interaction):
        msg: Message = interaction.message
        now = datetime.now()
        self.year = now.year
        self.month = now.month
        await self._refresh(msg)

    @button(label="Month →")
    async def next_month(self, btn: Button, interaction: Interaction):
        msg: Message = interaction.message
        self.month += 1
        await self._refresh(msg)

    @button(label="Year →")
    async def next_year(self, btn: Button, interaction: Interaction):
        msg: Message = interaction.message
        self.year += 1
        await self._refresh(msg)

    async def _refresh(self, msg: Message):
        await msg.edit(
            content=f"```"
                    f"{self.calendar.formatmonth(self.year, self.month, 3)}"
                    f"```",
            view=self
        )
