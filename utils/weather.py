WEATHER_ICONS = {
    '01d': 'clear',
    '01n': 'clear_night',
    '02d': 'few_clouds',
    '02n': 'few_clouds_night',
    '03d': 'clouds',
    '03n': 'clouds',
    '04d': 'clouds',
    '04n': 'clouds',
    '09d': 'shower_rain',
    '09n': 'shower_rain',
    '10d': 'rain',
    '10n': 'rain_night',
    '11d': 'thunderstorm',
    '11n': 'thunderstorm',
    '13d': 'snow',
    '13n': 'snow',
    '50d': 'mist',
    '50n': 'mist'
}
DEGREE_SYMBOL = u'\N{DEGREE SIGN}'


def get_weather_icon_name(icon: str) -> str:
    if icon in WEATHER_ICONS:
        return WEATHER_ICONS.get(icon)
    print(f"Error: Unable to retrieve weather icon for '{icon}'")
    # TODO: return error icon
    return None
