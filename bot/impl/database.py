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
import os
import typing

import mysql.connector

from bot.proto.database import UserSettings
from module_services.bot import BotService


def connect_to_database(
    password: str, url: str, user: str, database: str
) -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(
        user=user, host=url, password=password, database=database
    )


class DatabaseImpl(BotService):
    def __init__(self, connection: mysql.connector.MySQLConnection):
        self._conn = connection
        self._logger = logging.getLogger(__name__)
        cursor = self._conn.cursor()
        self._conn.commit()
        cursor.close()

    @classmethod
    def connect(cls):
        conn = connect_to_database(
            password=os.getenv("DATABASE_PASSWORD"),
            url=os.getenv("DATABASE_URL"),
            user=os.getenv("DATABASE_USERNAME"),
            database=os.getenv("DATABASE_NAME"),
        )
        return cls(conn)

    def set_setting(self, user: int, setting: str, value: typing.Any):
        cursor = self._conn.cursor()
        cursor.execute(
            f"""
            insert into settings (id, {setting}) values ({user}, "{value}")
            on duplicate key update {setting}="{value}"
            """
        )
        self._conn.commit()
        cursor.close()

    def get_setting(self, user: int, setting: str) -> typing.Any:
        cursor = self._conn.cursor()
        cursor.execute(
            f"""
            select ({setting}) from settings where id={user}
            """
        )
        row = cursor.fetchone()
        if not row:
            cursor.execute(f"insert into settings (id) values ({user})")
            self._conn.commit()
        cursor.close()
        return row[0] if row else "f"

    def get_settings(self, user: int) -> UserSettings:
        cursor = self._conn.cursor()
        cursor.execute(
            f"""
            select * from settings where id={user}
            """
        )
        row = cursor.fetchone()
        if not row:
            cursor.execute(f"insert into settings (id) values ({user})")
            self._conn.commit()
        cursor.close()
        return (
            UserSettings(row[0], row[1] == "i")
            if row
            else UserSettings(user, True)
        )
