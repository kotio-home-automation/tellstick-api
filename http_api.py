'''
HTTP API for providing tellstick switch status

Endpoints:
    list switches: http://0.0.0.0:5001/tellstick/switches
    list known sensors: http://0.0.0.0:5001/tellstick/sensors
    turn on switches: http://0.0.0.0:5001/tellstick/on
    turn off switches: http://0.0.0.0:5001/tellstick/off

Requires:
    bottle
    tellcore-py
'''
from bottle import get, post, response, request, run
import json
import tellcore.telldus as td
from device.device import list_devices, turn_off, turn_on
from sensor.sensor import list_sensors, load_sensor_configuration

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

@get('/tellstick/switches')
@enable_cors
def list_device_data():
    response.content_type = 'application/json; charset=UTF-8'
    return list_devices(core.devices())

@post('/tellstick/on')
def turn_on_devices():
    response.content_type = 'application/json; charset=UTF-8'
    deviceIds = request.json
    turn_on(deviceIds, core.devices())
    return list_devices(core.devices())

@post('/tellstick/off')
def turn_off_devices():
    response.content_type = 'application/json; charset=UTF-8'
    deviceIds = request.json
    turn_off(deviceIds, core.devices())
    return list_devices(core.devices())

@get('/tellstick/sensors')
@enable_cors
def list_sensor_data():
    response.content_type = 'application/json; charset=UTF-8'
    sensorConfiguration = load_sensor_configuration('sensors.json')
    return list_sensors(core.sensors(), sensorConfiguration)

if __name__ == '__main__':
    try:
        run(host='0.0.0.0', port=5001, debug=True)
    except:
        pass
