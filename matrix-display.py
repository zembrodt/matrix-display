# matrix-display
from datetime import datetime
from flask import Flask, request, jsonify, make_response, Response
from config import LED_ROWS, LED_COLS, LED_SLOWDOWN_GPIO, LED_BRIGHTNESS
from data import mlb_teams
from display import RGBDisplay
import signal
from enum import Enum
import sys


class Cache(Enum):
    DISPLAY = 1


def create_display() -> RGBDisplay:
    return RGBDisplay(LED_ROWS, LED_COLS, slowdown_gpio=LED_SLOWDOWN_GPIO, brightness=LED_BRIGHTNESS)


app = Flask(__name__, template_folder='resources/templates')

cache = {}


def stop_display():
    if Cache.DISPLAY not in cache:
        display = create_display()
        cache[Cache.DISPLAY] = display
    elif cache[Cache.DISPLAY].running:
        cache[Cache.DISPLAY].stop()


def create_args(data):
    kwargs = {}
    if 'date' in data:
        kwargs['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
    if 'team' in data:
        kwargs['team'] = data['team']
    if 'zip_code' in data:
        kwargs['zip_code'] = int(data['zip_code'])
    return kwargs


def _check_cors() -> Response:
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    return None


@app.route('/scene', methods=['POST', 'OPTIONS'])
def scene():
    response = _check_cors()
    if response:
        return response

    if request.method == 'POST':
        data = request.json
        args = create_args(data)
        if 'scene' in data:
            stop_display()
            cache[Cache.DISPLAY].set_scene(data['scene'], **args)
            cache[Cache.DISPLAY].start()
            response = jsonify(statusCode=200, message='Success')
        else:
            response = jsonify(statusCode=400, message='Missing required parameter [scene]')
    else:
        response = jsonify(statusCode=405, message='Method not allowed')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/stop', methods=['POST'])
def stop():
    response = _check_cors()
    if response:
        return response

    if request.method == 'POST':
        print(f'Hit endpoint {"/stop"}')
        if Cache.DISPLAY in cache:
            if cache[Cache.DISPLAY].stop():
                response = jsonify(statusCode=200, message='Success')
            else:
                response = jsonify(statusCode=403, message='Unable to stop display')
        else:
            response = jsonify(statusCode=200, message='No display to stop')
    else:
        response = jsonify(statusCode=405, message='Method not allowed')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/mlb/teams', methods=['GET'])
def get_mlb_teams():
    response = _check_cors()
    if response:
        return response

    if request.method == 'GET':
        response = jsonify(mlb_teams)
    else:
        response = jsonify(statusCode=405, message='Method not allowed')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def _quit_display(signum, frame):
    if Cache.DISPLAY in cache:
        if cache[Cache.DISPLAY].stop():
            print('Display stopped')
        else:
            print('Error: unable to stop display')
    sys.exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _quit_display)
    signal.signal(signal.SIGTERM, _quit_display)
    app.run(host='0.0.0.0', port=8080)
