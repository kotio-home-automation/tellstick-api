'''
HTTP API for providing tellstick switch status

Endpoints:
    list switches: http://0.0.0.0:5001/tellstick/switches
    list known sensors: http://0.0.0.0:5001/tellstick/sensors
    turn on switches: TODO
    turn off switches: TODO

Requires:
    bottle
    tellcore-py
'''

from bottle import get, response, request, run
import json
import tellcore.telldus as td
import tellcore.constants as const

core = td.TelldusCore()
sensorConfiguration = [
    {'id': 135, 'name': 'Olohuone'},
    {'id': 136, 'name': 'Parveke'}
]

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

def parseSwitchData(device):
    cmd = device.last_sent_command(const.TELLSTICK_TURNON | const.TELLSTICK_TURNOFF | const.TELLSTICK_DIM)
    return {'id': device.id, 'name': device.name, 'switchedOn': cmd == const.TELLSTICK_TURNON}

def list_switches():
    allSwitchesData = map(parseSwitchData, core.devices())
    return json.dumps(list(allSwitchesData), ensure_ascii=False).encode('utf8')

def findCurrentSensorName(sensorId):
    matchingSensorsConfiguration = filter(lambda knownSensor: knownSensor['id'] == sensorId, sensorConfiguration)
    currentSensorConfiguration = next(matchingSensorsConfiguration)
    return currentSensorConfiguration['name']

def parseSensorData(sensor):
    humidity = sensor.value(const.TELLSTICK_HUMIDITY) if sensor.has_value(const.TELLSTICK_HUMIDITY) else None
    temperature = sensor.value(const.TELLSTICK_TEMPERATURE)
    name = findCurrentSensorName(sensor.id)
    
    if humidity is None:
        return {'id': sensor.id, 'name': name, 'temperature': float(temperature.value)}
    else:
        return {'id': sensor.id, 'name': name, 'temperature': float(temperature.value), 'humidity': float(humidity.value)}

def filter_known_sensors(sensor):
    knownSensorIds = map(lambda knownSensor: knownSensor['id'], sensorConfiguration)
    return sensor.id in knownSensorIds

def list_sensors():
    sensors = filter(filter_known_sensors, core.sensors())
    allSensorsData = map(parseSensorData, sensors)
    return json.dumps(list(allSensorsData), ensure_ascii=False).encode('utf8')

@get('/tellstick/switches')
@enable_cors
def list_switch_data():
    response.content_type = 'application/json; charset=UTF-8'
    return list_switches()

@get('/tellstick/sensors')
@enable_cors
def list_sensor_data():
    response.content_type = 'application/json; charset=UTF-8'
    return list_sensors()

if __name__ == '__main__':
    try:
        run(host='0.0.0.0', port=5001, debug=True)
    except:
        pass
