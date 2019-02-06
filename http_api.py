'''
HTTP API for providing tellstick switch status

Endpoints:
    list switches: http://0.0.0.0:5001/tellstick/devices
    list known sensors: http://0.0.0.0:5001/tellstick/sensors
    turn on switches: http://0.0.0.0:5001/tellstick/devices/on
    turn off switches: http://0.0.0.0:5001/tellstick/devices/off

Requires:
    bottle
    tellcore-py

Start with command: python3 http_api.py sensors.json
'''
from bottle import get, post, response, request, run
import json, sys
import tellcore.telldus as td
from device.device import list_devices, turn_off, turn_on
from sensor.sensor import TellstickSensor

core = td.TelldusCore()

# borrowed from https://ongspxm.github.io/blog/2017/02/bottlepy-cors/
def enable_cors(func):
    def wrapper(*args, **kwargs):
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        response.set_header("Access-Control-Allow-Headers", "Origin, Content-Type")

        # skip the function if it is not needed
        if request.method == 'OPTIONS':
            return

        return func(*args, **kwargs)

    return wrapper

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        print('Too many arguments!')
        sys.exit(0)

    # First argument is this python file itself
    if (len(sys.argv) == 2):
        configurationFile = sys.argv[1]
        global tellstickSensor
        tellstickSensor = TellstickSensor(configurationFile)

@get('/tellstick/devices')
@enable_cors
def list_device_data():
    response.content_type = 'application/json; charset=UTF-8'
    return list_devices(core.devices())

@post('/tellstick/devices/on')
def turn_on_devices():
    response.content_type = 'application/json; charset=UTF-8'
    deviceIds = request.json
    turn_on(deviceIds, core.devices())
    return list_devices(core.devices())

@post('/tellstick/devices/off')
def turn_off_devices():
    response.content_type = 'application/json; charset=UTF-8'
    deviceIds = request.json
    turn_off(deviceIds, core.devices())
    return list_devices(core.devices())

@get('/tellstick/sensors')
@enable_cors
def list_sensor_data():
    response.content_type = 'application/json; charset=UTF-8'
    return tellstickSensor.list_sensors(core.sensors())

if __name__ == '__main__':
    try:
        run(host='0.0.0.0', port=5001, debug=True)
    except:
        pass
