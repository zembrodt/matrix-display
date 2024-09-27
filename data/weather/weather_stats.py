from PIL import Image
from api.weather_api import WeatherApi
from models.weather.weather import WeatherData

_ICON_WIDTH = 10
_ICON_HEIGHT = 10


class WeatherStats:
    def __init__(self, zip_code: int):
        self._zip_code: int = zip_code
        self._data: WeatherData = None
        self.refresh_data()
        self._icon: Image = None
        self._prev_icon_name: str = None

    def refresh_data(self):
        self._data = WeatherApi.get_current_weather(zip_code=self._zip_code)

    def _load_icon(self, width: int = _ICON_WIDTH, height: int = _ICON_HEIGHT):
        if self.data and (not self._icon or self.data.icon_name != self._prev_icon_name):
            self._icon = Image.open(f'resources/images/weather/{self.data.icon_name}.png')
            self._icon.thumbnail((width, height), Image.ANTIALIAS)
            self._icon = self._icon.convert('RGB')
            self._prev_icon_name = self.data.icon_name
        return self._icon

    @property
    def data(self) -> WeatherData:
        if not self._data:
            self.refresh_data()
        return self._data

    @property
    def zip_code(self) -> int:
        return self._zip_code

    @property
    def icon(self) -> Image:
        return self._load_icon()
