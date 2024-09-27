from typing import List

from PIL import Image
from api.weather_api import WeatherApi
from models.weather.weather import WeatherData

_ICON_WIDTH = 10
_ICON_HEIGHT = 10


class ForecastStats:
    def __init__(self, zip_code: int):
        self._zip_code: int = zip_code
        self._forecasts: List[WeatherData] = []
        self._forecast_icons = dict()
        self.refresh_data()
        self._icon: Image = None

    def refresh_data(self):
        self._forecasts = WeatherApi.get_forecasted_weather(self._zip_code, days=3, forecasted_hour=11)
        for forecast in self._forecasts:
            if forecast.icon_name not in self._forecast_icons:
                icon = Image.open(f'resources/images/weather/{forecast.icon_name}.png')
                icon.thumbnail((_ICON_WIDTH, _ICON_HEIGHT), Image.ANTIALIAS)
                icon = icon.convert('RGB')
                self._forecast_icons[forecast.icon_name] = icon

    def get_icon(self, icon_name: str) -> Image:
        if icon_name in self._forecast_icons:
            return self._forecast_icons[icon_name]
        return None

    @property
    def data(self) -> List[WeatherData]:
        if not self._forecasts:
            self.refresh_data()
        return self._forecasts

    @property
    def zip_code(self) -> int:
        return self._zip_code
