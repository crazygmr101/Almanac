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
from datetime import timedelta
from io import BytesIO

import aiohttp
from PIL import Image
from yarl import URL

from libs.disk_cache import DiskCache
from libs.helpers import get_tiles, assemble_mosaic


class MapTilerAPI:
    def __init__(self, token: str):
        self.token = token
        self.satellite_disk_cache = DiskCache(
            "/tmp/almanac/map-tiler", timedelta(days=7)
        )

    async def _map_tile(
        self, x: int, y: int, zoom: int, path: str, ext: str
    ) -> Image.Image:
        resp = self.satellite_disk_cache.get(f"{path}/{zoom}/{x}/{y}.jpg")
        buf = BytesIO()
        if resp is not None:
            buf.write(resp)
            buf.seek(0)
        else:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    url=URL.build(
                        scheme="https",
                        host="api.maptiler.com",
                        path=f"{path}/{zoom}/{x}/{y}.{ext}",
                        query={"key": self.token},
                    ),
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/91.0.4472.114 Safari/537.36"
                    },
                ) as resp:
                    buf.write(await resp.read())
            buf.seek(0)
            self.satellite_disk_cache.put(
                f"{path}/{zoom}/{x}/{y}.{ext}", buf.read()
            )
            buf.seek(0)
        img: Image.Image = Image.open(buf)
        img.load()
        img = img.convert("RGBA")
        return img

    async def get_map_image(
        self, lat: float, lon: float, zoom: int
    ) -> Image.Image:
        tiles, location = get_tiles(lat, lon, zoom)
        satellite_images = [
            await self._map_tile(
                tile[0], tile[1], zoom, "/maps/hybrid/256", "jpg"
            )
            for tile in [
                (tiles[0], tiles[1]),
                (tiles[0], tiles[3]),
                (tiles[2], tiles[1]),
                (tiles[2], tiles[3]),
            ]
        ]
        hillshade_images = [
            await self._map_tile(
                tile[0], tile[1], zoom, "/tiles/hillshades", "png"
            )
            for tile in [
                (tiles[0], tiles[1]),
                (tiles[0], tiles[3]),
                (tiles[2], tiles[1]),
                (tiles[2], tiles[3]),
            ]
        ]
        satellite_assembled = assemble_mosaic(satellite_images, location)
        hillshade_assembled = assemble_mosaic(hillshade_images, location)
        return Image.alpha_composite(satellite_assembled, hillshade_assembled)
