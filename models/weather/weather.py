from datetime import datetime
from utils.weather import get_weather_icon_name


class WeatherData:
    def __init__(self, data, city_name: str = None):
        self._city_name: str = data['name'] if 'name' in data else city_name
        self._icon_name: str = get_weather_icon_name(data['weather'][0]['icon'])
        self._temp: float = float(data['main']['temp'])
        self._feels_like: float = float(data['main']['feels_like'])
        self._temp_min: float = float(data['main']['temp_min'])
        self._temp_max: float = float(data['main']['temp_max'])
        self._humidity: float = float(data['main']['humidity'])
        self._wind_speed: int = data['wind']['speed']
        if 'clouds' in data:
            self._cloud_coverage: float = data['clouds']['all']
        if 'rain' in data:
            self._rain_volume: float = WeatherData._get_volume(data['rain'])
        if 'snow' in data:
            self._snow_volume: float = WeatherData._get_volume(data['snow'])
        self._timestamp: datetime = datetime.fromtimestamp(data['dt'])

    @property
    def city_name(self) -> str:
        return self._city_name

    @property
    def icon_name(self) -> str:
        return self._icon_name

    @property
    def temp(self) -> int:
        return round(self._temp)

    @property
    def feels_like(self) -> int:
        return round(self._feels_like)

    @property
    def temp_min(self) -> int:
        return round(self._temp_min)

    @property
    def temp_max(self) -> int:
        return round(self._temp_max)

    @property
    def humidity(self) -> int:
        return round(self.humidity)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @staticmethod
    def _get_volume(data) -> float:
        if '3h' in data:
            return data['3h']
        elif '1h' in data:
            return data['1h']
        else:
            return None
