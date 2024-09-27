from datetime import datetime, timedelta
from data import WeatherStats
from scenes.scene import Scene
from utils.colors import *
from utils.weather import DEGREE_SYMBOL


class WeatherScene(Scene):
    name = 'weather'
    _weather_refresh_delay = timedelta(minutes=15)

    def __init__(self, canvas, zip_code=90210):
        super().__init__(canvas)
        self._prev_time: datetime = None
        self._zip_code: int = zip_code
        self._current_weather: WeatherStats = WeatherStats(self._zip_code)

    def _check_if_refresh_required(self):
        return self._prev_refresh_time is None or self._now - self._prev_refresh_time >= self._weather_refresh_delay

    def _refresh_data(self):
        print(f'Refreshing weather data: {self._now.strftime("%Y-%m-%d %H:%M:%S")}')
        self._current_weather.refresh_data()

    def display(self):
        # Display the current data
        self._canvas.draw_image(8, 2, self._current_weather.icon)
        temp_color = text_color_yellow
        if self._current_weather.data.temp > 80:
            temp_color = text_color_red
        elif self._current_weather.data.temp < 50:
            temp_color = text_color_blue
        self._canvas.draw_text_md_bold(4, 24, f'{self._current_weather.data.temp}{DEGREE_SYMBOL}', temp_color)
        min_length = self._canvas.draw_text_xs(3, 32, str(self._current_weather.data.temp_min), text_color_blue)
        self._canvas.draw_text_xs(min_length + 6, 32, str(self._current_weather.data.temp_max), text_color_red)

        # Display current date
        date = self._now.strftime('%d %b')
        self._canvas.draw_text_sm(28, 26, date, text_color_yellow)

        # Display current time
        curr_time_hours = int(self._now.strftime('%I'))
        curr_time_of_day = 'a' if self._now.hour < 12 else 'p'
        curr_time_minutes = self._now.strftime('%M')
        pos_x = 22 if curr_time_hours >= 10 else 29
        self._canvas.draw_text_lg_bold(pos_x, 12, f'{curr_time_hours}:{curr_time_minutes}{curr_time_of_day}',
                                       text_color_yellow)

    def _refresh_display_required(self) -> bool:
        if self._prev_time is None or self._prev_time.minute != self._now.minute:
            self._prev_time = self._now
            return True
        return False
