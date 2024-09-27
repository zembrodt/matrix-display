from datetime import datetime
from typing import List, Union

import requests

from config import OPEN_WEATHER_API_KEY
from models.weather import WeatherData


class WeatherApi:
    @staticmethod
    def get_current_weather(zip_code: int, country: str = 'us', units: str = 'imperial') -> Union[WeatherData, None]:
        response = requests.get(WeatherApi._get_weather_url(zip_code, country=country, units=units))
        if response.status_code == 200:
            return WeatherData(response.json())
        return None

    @staticmethod
    def get_forecasted_weather(zip_code, country='us', units='imperial', days=5, forecasted_hour=None) -> List[WeatherData]:
        if days < 5 and forecasted_hour >= datetime.now().hour:
            days += 1
        response = requests.get(WeatherApi._get_forecast_url(zip_code, country=country, units=units, days=days))
        if response.status_code == 200:
            raw_data = response.json()
            city_name = raw_data['city']['name']
            forecasts_raw = raw_data['list']
            forecasts_total = [WeatherData(forecast, city_name) for forecast in forecasts_raw]
            if forecasted_hour is not None:
                return WeatherApi._filter_forecasts(forecasts_total, at_hour=forecasted_hour)
            return forecasts_total
        return []

    @staticmethod
    def _get_weather_url(zip_code: int, country: str = 'us', units: str = 'imperial') -> str:
        return f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country}&units={units}&appid={OPEN_WEATHER_API_KEY}'

    @staticmethod
    def _get_forecast_url(zip_code: int, country: str = 'us', units: str = 'imperial', days: int = 5) -> str:
        if days > 5:
            days = 5
        elif days < 1:
            days = 1
        return f'https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country}&units={units}&cnt={days * 8}&appid={OPEN_WEATHER_API_KEY}'

    @staticmethod
    def _filter_forecasts(forecasts: List[WeatherData], at_hour: int = 11) -> List[WeatherData]:
        now = datetime.now()
        return list(filter(
            lambda forecast: (forecast.timestamp > now and forecast.timestamp.day != now.day) and forecast.timestamp.hour == at_hour, forecasts))
