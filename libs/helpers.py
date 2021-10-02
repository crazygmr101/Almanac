import math
from typing import Tuple, List

from PIL import Image, ImageDraw


def get_tiles(
    lat: float, lon: float, zoom: int
) -> Tuple[Tuple[int, int, int, int], Tuple[int, int]]:  # noqa e124
    n = 2.0 ** zoom
    x = (lon + 180.0) / 360.0 * n
    y = (
        (
            1.0
            - math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat))))
            / math.pi
        )
        / 2.0
        * n
    )
    # x and y are float coords here, grab whatever other tiles i need
    # other bounds
    x2 = x - 1 if x - int(x) < 0.5 else x + 1
    y2 = y - 1 if y - int(y) < 0.5 else y + 1

    # make sure they're always in the right order
    x1, x2 = (int(x), int(x2)) if x < x2 else (int(x2), int(x))
    y1, y2 = (int(y), int(y2)) if y < y2 else (int(y2), int(y))

    # map tiles are 256x256 so grab the coords the location is on the pic
    center_x = max(x1, x2)
    center_y = max(y1, y2)
    x_pos = int(256 + (x - int(center_x)) * 256)
    y_pos = int(256 + (y - int(center_y)) * 256)
    return ((x1, y1, x2, y2), (x_pos, y_pos))


def assemble_mosaic(
    images: List[Image.Image], location: Tuple[int, int]
) -> Image.Image:
    mosaic = Image.new("RGBA", (512, 512))
    mosaic.paste(images[0], (0, 0))
    mosaic.paste(images[1], (0, 256))
    mosaic.paste(images[2], (256, 0))
    mosaic.paste(images[3], (256, 256))
    mosaic = mosaic.crop(
        [location[0] - 128, location[1] - 128, location[0] + 128, location[1] + 128]
    )
    return mosaic
