from datetime import datetime, timedelta
from data import WeatherStats, ForecastStats
from scenes.weather import WeatherScene
from utils.colors import *
from utils.weather import DEGREE_SYMBOL

FORECAST_ICON_WIDTH = 8
FORECAST_ICON_HEIGHT = 8


class ForecastScene(WeatherScene):
    name = 'forecast'
    _forecast_refresh_delay = timedelta(hours=1)

    def __init__(self, canvas, zip_code=90210):
        super().__init__(canvas, zip_code)
        self._forecast_refresh_required = False
        self._forecasts: ForecastStats = ForecastStats(self._zip_code)

    def _check_if_refresh_required(self):
        self._forecast_refresh_required = self._prev_refresh_time is None or self._now - self._prev_refresh_time >= self._forecast_refresh_delay
        return super()._check_if_refresh_required() or self._forecast_refresh_required

    def _refresh_data(self):
        if self._forecast_refresh_required:
            print(f'Refreshing forecast data: {self._now.strftime("%Y-%m-%d %H:%M:%S")}')
            self._forecasts.refresh_data()
            self._forecast_refresh_required = False

    def display(self):
        # Display current data
        self._canvas.draw_image(1, 1, self._current_weather.icon)
        temp_color = text_color_yellow
        if self._current_weather.data.temp > 80:
            temp_color = text_color_red
        elif self._current_weather.data.temp < 50:
            temp_color = text_color_blue
        self._canvas.draw_text_sm(12, 8, f'{self._current_weather.data.temp}{DEGREE_SYMBOL}', temp_color)

        # Display current date
        date = self._now.strftime('%d %b')
        self._canvas.draw_text_xs(1, 16, date, text_color_yellow)

        # Display current time
        curr_time_minutes = self._now.strftime('%I:%M')
        self._canvas.draw_text_lg_bold(28, 12, f'{curr_time_minutes}', text_color_yellow)

        # Display forecasted data
        for i, forecast in enumerate(self._forecasts.data):
            self._canvas.draw_text_xs((i * 22) + 4, 22, forecast.timestamp.strftime('%a'), text_color_blue)
            self._canvas.draw_image(i * 22, 24, self._forecasts.get_icon(forecast.icon_name))
            self._canvas.draw_text_xs((i * 22) + 9, 30, f'{forecast.temp}{DEGREE_SYMBOL}', text_color_yellow)

    def _refresh_display_required(self) -> bool:
        if self._prev_time is None or self._prev_time.minute != self._now.minute:
            self._prev_time = self._now
            return True
        return False
