"""Screensaver selectors and texture aliases, independent of Kodi's GUI."""
import json
from pathlib import Path
import random

ROOT = 'special://home/addons/resource.images.arctic.splash/resources/'
STATES = {
    'season': ('summer', 'autumn', 'winter', 'spring'),
    'scene': ('fuji', 'countryside', 'tokyo'),
    'time': tuple(f'{hour:02d}00' for hour in range(24)),
    'weather': ('clear', 'partlycloudy', 'cloud', 'windy', 'rain', 'heavyrain',
                'snow', 'thunderstorm', 'severethunderstorm', 'hazy'),
}
MODES = {
    key: ('auto', 'random', 'specific') if key == 'scene' else ('auto', 'current', 'random', 'specific')
    for key in STATES
}
# Seconds per step. Every selector has its own clock; fixed modes never advance.
INTERVALS = {'season': 60, 'scene': 120, 'time': 10, 'weather': 30}
SOUTHERN_REGIONS = set(json.loads((Path(__file__).resolve().parents[1] / 'southern-regions.json').read_text(encoding='utf-8')))
WEATHER_CODES = {
    'severethunderstorm': {3}, 'windy': {23, 24},
    'thunderstorm': {0, 1, 2, 4, 37, 38, 39, 45, 47},
    'hazy': {19, 20, 21, 22}, 'heavyrain': {12},
    'rain': {6, 8, 9, 10, 11, 17, 18, 35, 40},
    'snow': {5, 7, 13, 14, 15, 16, 41, 42, 43, 46},
    'cloud': {26, 27, 28}, 'partlycloudy': {29, 30, 44},
}


def current_states(now, region, weather_code):
    """Match the splash's meteorological seasons and weather-code precedence."""
    seasons = ('winter', 'spring', 'summer', 'autumn')
    quarter = (now.month % 12) // 3
    if region.upper() in SOUTHERN_REGIONS:
        quarter = (quarter + 2) % 4
    try:
        code = int(weather_code)
    except (TypeError, ValueError):
        code = -1
    weather = next((state for state, codes in WEATHER_CODES.items() if code in codes), 'clear')
    return {'season': seasons[quarter], 'time': f'{now.hour:02d}00', 'weather': weather,
            'scene': STATES['scene'][0]}


class Selectors:
    def __init__(self, settings, current, started, choose=None):
        self.modes = {}
        self.values = {}
        self.started = started
        self.initial = {}
        choose = choose or random.choice
        for key, states in STATES.items():
            mode = settings.get(key + '.mode', 'auto')
            self.modes[key] = mode if mode in MODES[key] else 'auto'
            if self.modes[key] == 'random':
                value = choose(states)
            elif self.modes[key] == 'specific':
                value = settings.get(key + '.state')
                value = value if value in states else states[0]
            else:
                value = current[key]
            self.values[key] = value
            self.initial[key] = states.index(value)

    def update(self, elapsed, current):
        for key, mode in self.modes.items():
            if mode == 'current':
                self.values[key] = current[key]
            elif mode == 'auto':
                states = STATES[key]
                step = int(max(0, elapsed - self.started) // INTERVALS[key])
                self.values[key] = states[(self.initial[key] + step) % len(states)]
        return dict(self.values)


def render_properties(values):
    season, hour, weather = (values[key] for key in ('season', 'time', 'weather'))
    h = int(hour[:2])
    sky_hour = f'{h:02d}00' if 5 <= h <= 7 else f'{24-h:02d}00' if 17 <= h <= 19 else '0800' if 8 <= h <= 16 else '0000'
    cloud_hour = hour if 5 <= h <= 7 or 17 <= h <= 19 else '0800' if 8 <= h <= 16 else '0000'
    glow_hour = '0500' if h in (5, 7) else '0600' if h == 6 else '1700' if h in (17, 19) else '1800' if h == 18 else '0000'
    time_hour = hour if 5 <= h <= 7 or 17 <= h <= 19 else '0800' if 8 <= h <= 16 else '0000' if h < 5 else '2000'
    base = ('clear' if weather in ('clear', 'partlycloudy') else 'cloud' if weather in ('cloud', 'windy')
            else 'rain' if weather in ('rain', 'heavyrain', 'snow', 'thunderstorm', 'severethunderstorm') else 'hazy')
    conditions = ('storm' if 'thunderstorm' in weather else 'rain' if weather in ('rain', 'heavyrain')
                  else 'snow' if weather == 'snow' else 'hazy' if weather == 'hazy' else 'cloud' if base == 'cloud' else 'none')
    return {
        'Season': season, 'Hour': hour, 'Weather': weather, 'Scene': values['scene'],
        'BaseWeather': base, 'Conditions': conditions, 'SkyHour': sky_hour,
        'CloudHour': cloud_hour, 'GlowHour': glow_hour,
        'ConditionsHour': '0000' if base == 'clear' else sky_hour,
        'TimeHour': time_hour, 'Sky': ROOT + 'layers/01-sky/' + sky_hour + '.jpg',
        'TimeTexture': ROOT + 'layers/09-time/' + ('autumn' if 8 <= h <= 16 else season) + '/' + time_hour + '.webp',
        'CloudColor': '1affffff' if weather == 'clear' else '99ffffff' if weather == 'partlycloudy' else 'e6ffffff' if base == 'cloud' else 'ffffffff',
        'ReflectionColor': '04ffffff' if weather == 'clear' else '17ffffff' if weather == 'partlycloudy' else '22ffffff' if base == 'cloud' else '26ffffff',
        'RippleColor': '26ffffff' if season == 'winter' else 'ffffffff',
    }
