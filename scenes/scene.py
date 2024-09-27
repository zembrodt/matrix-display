import time
from datetime import datetime
from canvas import Canvas


class Scene:
    def __init__(self, canvas: Canvas):
        self._canvas: Canvas = canvas
        self._now: datetime = datetime.now()
        self._prev_refresh_time: datetime = None
        self._data_refreshed = False

    def refresh_data(self):
        self._now = datetime.now()
        if self._check_if_refresh_required():
            self._refresh_data()
            self._data_refreshed = True
            self._prev_refresh_time = datetime.now()

    def _check_if_refresh_required(self) -> bool:
        pass

    def _refresh_data(self):
        pass

    def display(self):
        pass

    def refresh_display(self) -> bool:
        if self._data_refreshed or self._refresh_display_required():
            self._data_refreshed = False
            return True
        return False

    def _refresh_display_required(self) -> bool:
        pass
