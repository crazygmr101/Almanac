import os
from datetime import datetime

from libs.googlemaps import GoogleMapsAPI
from libs.openweathermap import OpenWeatherMapAPI, CityNotFoundError
from module_services.bot import BotService


# noinspection PyMethodMayBeStatic
class WeatherService(BotService):
    def __init__(self):
        self.owm_api = OpenWeatherMapAPI(os.getenv("OWM"))
        self.gmaps_api = GoogleMapsAPI(os.getenv("GMAPS"))

    async def current_conditions(self, city: str):
        try:
            conditions = await self.owm_api.get_current_conditions(city)
        except CityNotFoundError:
            if city.lower() == "mordor":
                return self.error_embed("City not found", "One does not simply look up Mordor's weather.")
            return self.error_embed("City not found", f"{city} seems to be an invalid city.")
        sunrise = datetime.utcfromtimestamp(conditions.sys.sunrise + conditions.timezone).strftime("%-I:%M %p")
        sunset = datetime.utcfromtimestamp(conditions.sys.sunset + conditions.timezone).strftime("%-I:%M %p")
        embed = self.ok_embed(title=f"**Conditions for {conditions.city_name}, {conditions.sys.country}**\n",
                              description=f"🏙 {conditions.weather[0].description.title()}\n"
                                          f"🌡️ **{int(conditions.main.temp)}**°F "
                                          f"(feels like **{int(conditions.main.feels_like)}**°)\n"
                                          f"🌅 **Sunrise**: {sunrise}\n"
                                          f"🌇 **Sunset**: {sunset}\n"
                                          f"🌬️ **{int(conditions.wind.speed)}** MPH from "
                                          f"{self.direction_for(conditions.wind.direction)}") \
            .set_thumbnail(url=self.icon_url_for(conditions.weather[0].icon)) \
            .set_footer(text="Powered by OpenWeatherMap")
        if conditions.snow:
            embed = embed.add_field(name="Snowfall", inline=True,
                                    value=f"❄️️ **1 hour**: {round(conditions.snow.one_hour, 2)} in"
                                          f"🌨️ **3 hour**: {round(conditions.snow.three_hour, 2)} in")
        if conditions.rain:
            embed = embed.add_field(name="Rainfall", inline=True,
                                    value=f"💧 **1 hour**: {round(conditions.rain.one_hour, 1)} in"
                                          f"🌧 **3 hour**: {round(conditions.rain.three_hour, 1)} in")
        return embed

    def icon_url_for(self, icon: str) -> str:
        return f"http://openweathermap.org/img/wn/{icon}@2x.png"

    def direction_for(self, deg: int):
        # see https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f#gistcomment-3070256
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(deg / (360. / len(dirs)))
        return dirs[ix % len(dirs)]
