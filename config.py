import tomllib

_DEFAULT_LED_ROWS = 32
_DEFAULT_LED_COLS = 32
_DEFAULT_LED_SLOWDOWN_GPIO = 1
_DEFAULT_LED_BRIGHTNESS = 50

with open('resources/config/config.toml', 'rb') as f:
    _config = tomllib.load(f)
    OPEN_WEATHER_API_KEY: str = _config.get('OPEN_WEATHER_API_KEY')
    LED_ROWS: int = _config.get('LED_ROWS') if _config.get('LED_ROWS') else _DEFAULT_LED_ROWS
    LED_COLS: int = _config.get('LED_COLS') if _config.get('LED_COLS') else _DEFAULT_LED_COLS
    LED_SLOWDOWN_GPIO: int = _config.get('LED_SLOWDOWN_GPIO') \
        if _config.get('LED_SLOWDOWN_GPIO') else _DEFAULT_LED_SLOWDOWN_GPIO

    _brightness_config: int = _config.get('LED_BRIGHTNESS')
    if not _brightness_config:
        _brightness_config = _DEFAULT_LED_BRIGHTNESS
    else:
        if _brightness_config < 0:
            _brightness_config = 0
        elif _brightness_config > 100:
            _brightness_config = 100
    LED_BRIGHTNESS: int = _brightness_config
