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
from io import BytesIO

import aiohttp
from PIL import Image
from yarl import URL


class MapTilerAPI:
    def __init__(self, token: str):
        self.token = token

    async def get_map_tile(self, x: int, y: int, zoom: int) -> Image.Image:
        # hhttps://api.maptiler.com/tiles/satellite/{z}/{x}/{y}.jpg
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url=URL.build(
                    scheme="https",
                    host="api.maptiler.com",
                    path=f"/tiles/satellite/{zoom}/{x}/{y}.jpg",
                    query={
                        "key": self.token
                    }
            ), headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"  # noqa e501
            }) as resp:
                buf = BytesIO()
                buf.write(await resp.read())
        buf.seek(0)
        img: Image.Image = Image.open(buf)
        img.load()
        img = img.convert("RGBA")
        return img
