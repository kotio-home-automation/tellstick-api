import json
import tellcore.constants as const

def __findCurrentSensorName(sensorId, sensorConfiguration):
    matchingSensorsConfiguration = filter(lambda knownSensor: knownSensor['id'] == sensorId, sensorConfiguration)
    currentSensorConfiguration = next(matchingSensorsConfiguration)
    return currentSensorConfiguration['name']

def __parseSensorData(sensor):
    humidity = sensor.value(const.TELLSTICK_HUMIDITY) if sensor.has_value(const.TELLSTICK_HUMIDITY) else None
    temperature = sensor.value(const.TELLSTICK_TEMPERATURE)
    
    if humidity is None:
        return {'id': sensor.id, 'temperature': float(temperature.value)}
    else:
        return {'id': sensor.id, 'temperature': float(temperature.value), 'humidity': float(humidity.value)}

def __appendNameToSensors(sensors, sensorConfiguration):
    namedSensors = []
    for sensor in sensors:
        filteredSensorConfigurations = filter(lambda c: c['id'] == sensor['id'], sensorConfiguration)
        configuration = next(filteredSensorConfigurations)
        sensor['name'] = configuration['name']
        namedSensors.append(sensor)

    return namedSensors

def __parseSensorsData(sensors, sensorConfiguration):
    parsedSensors = map(__parseSensorData, sensors)
    namedSensors = __appendNameToSensors(parsedSensors, sensorConfiguration)
    return namedSensors

def __filter_known_sensors(sensors, sensorConfiguration):
    knownSensorIds = map(lambda knownSensor: knownSensor['id'], sensorConfiguration)
    knownSensors = filter(lambda sensor: sensor.id in knownSensorIds, sensors)
    return knownSensors

def list_sensors(sensors, sensorConfiguration):
    knownSensors = __filter_known_sensors(sensors, sensorConfiguration)
    parsedSensorData = __parseSensorsData(knownSensors, sensorConfiguration)
    return json.dumps(parsedSensorData, ensure_ascii=False).encode('utf8')

def load_sensor_configuration(fileName):
    with open(fileName) as sensorConfigurationFile:
        configuredSensors = json.load(sensorConfigurationFile)
    sensorConfigurationFile.close()
    return configuredSensors
