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
from typing import Union


def cloud_coverage_label(coverage: int) -> str:
    return (
        "Clear"
        if coverage < 12
        else "Mostly Sunny"
        if coverage < 40
        else "Partly Cloudy"
        if coverage < 65
        else "Mostly Cloudy"
        if coverage < 90
        else "Overcast"
    )


def cloud_icon_url_for(icon: str) -> str:
    return f"http://openweathermap.org/img/wn/{icon}@2x.png"


def direction_for(deg: Union[int, float]):
    # see https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f#gistcomment-3070256
    dirs = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    ix = round(deg / (360.0 / len(dirs)))
    return dirs[ix % len(dirs)]
