from scenes.scene import Scene
from utils.colors import text_color_yellow
from datetime import datetime


class ClockScene(Scene):
    name = 'clock'

    def __init__(self, canvas):
        super().__init__(canvas)
        self._prev_time: datetime = None

    def _check_if_refresh_required(self) -> bool:
        return False

    def _refresh_data(self):
        pass

    def display(self):
        print('Showing display!')
        curr_date = self._now.strftime('%a, %b %d')
        curr_time = self._now.strftime('%H:%M:%S')
        self._canvas.draw_text_xs(2, 6, curr_date, text_color_yellow)
        self._canvas.draw_text_lg_bold(4, 20, curr_time, text_color_yellow)

    def _refresh_display_required(self) -> bool:
        if self._prev_time is None or self._prev_time.second != self._now.second:
            self._prev_time = self._now
            return True
        return False

