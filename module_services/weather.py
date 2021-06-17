import os
from datetime import datetime

from libs.openweathermap import OpenWeatherMapAPI, CityNotFoundError
from module_services.bot import BotService


# noinspection PyMethodMayBeStatic
class WeatherService(BotService):
    def __init__(self):
        self.api = OpenWeatherMapAPI(os.getenv("OWM"))

    async def current_conditions(self, city: str):
        try:
            conditions = await self.api.get_current_conditions(city)
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
        return embed

    def icon_url_for(self, icon: str) -> str:
        return f"http://openweathermap.org/img/wn/{icon}@2x.png"

    def direction_for(self, deg: int):
        # see https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f#gistcomment-3070256
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(deg / (360. / len(dirs)))
        return dirs[ix % len(dirs)]