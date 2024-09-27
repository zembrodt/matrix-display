import time
import threading
from datetime import datetime
from canvas import Canvas
from scenes import ForecastScene, ClockScene, WeatherScene, MlbGameScene, Scene
from scenes.nfl_game import NflGameScene


class RGBDisplay:
    def __init__(self, rows: int, cols: int, brightness: int = 100, show_refresh: bool = False,
                 slowdown_gpio: int = 1):
        self._state = threading.Event()
        self._thread: threading.Thread = None
        self._canvas: Canvas = Canvas(rows, cols, brightness=brightness, show_refresh=show_refresh, slowdown_gpio=slowdown_gpio)
        self._scene: Scene = None

    def _run(self, state: threading.Event):
        print('Running matrix display...')

        self._scene.refresh_data()

        while not state.is_set():
            self._scene.refresh_data()

            if self._scene.refresh_display():
                self._canvas.clear()
                self._scene.display()
                self._canvas.swap_on_vsync()

            time.sleep(0.05)
        print('Exiting running state and clearing display...')
        self._canvas.clear()
        self._canvas.swap_on_vsync()

    def start(self) -> bool:
        if self._thread is None or not self._thread.is_alive():
            self._state.clear()
            print('Starting process thread')
            self._thread = threading.Thread(target=self._run, args=(self._state,))
            self._thread.start()
            return True
        return False

    def stop(self) -> bool:
        if self._thread is not None and not self._state.is_set():
            self._state.set()
            print('Stopped thread')
            self._thread.join()
            print('Re-joined thread')
            return True
        return False

    def set_scene(self, scene: str, **kwargs):
        if scene == WeatherScene.name:
            self._scene = WeatherScene(self._canvas, zip_code=kwargs['zip_code'])
        elif scene == ForecastScene.name:
            self._scene = ForecastScene(self._canvas, zip_code=kwargs['zip_code'])
        elif scene == ClockScene.name:
            self._scene = ClockScene(self._canvas)
        elif scene == MlbGameScene.name:
            date = kwargs['date'] if 'date' in kwargs else datetime.now()
            print(f'Using team {kwargs["team"]} on date {date}')
            self._scene = MlbGameScene(self._canvas, kwargs['team'], date)
        elif scene == NflGameScene.name:
            self._scene = NflGameScene(self._canvas, team_name=kwargs['team'], game_id=kwargs['id'])
        else:
            print(f"Unknown scene '{scene}' requested. Exiting...")
            exit()

    @property
    def running(self) -> bool:
        return not self._state.is_set()
