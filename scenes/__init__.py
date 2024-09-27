from .clock import ClockScene
from .forecast import ForecastScene
from .mlb_game import MlbGameScene
from .scene import Scene
from .weather import WeatherScene

_SCENES = (
    ForecastScene.name,
    WeatherScene.name,
    ClockScene.name,
    MlbGameScene.name
)


def is_valid_scene(scene_name: str):
    return scene_name.strip().lower() in _SCENES
