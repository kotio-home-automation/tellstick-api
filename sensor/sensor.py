import json
import tellcore.constants as const

class TellstickSensor():

    def __init__(self, sensorConfigurationFile):
        self.sensorConfiguration = self.__load_sensor_configuration__(sensorConfigurationFile)

    def __load_sensor_configuration__(self, fileName):
        with open(fileName) as sensorConfigurationFile:
            configuredSensors = json.load(sensorConfigurationFile)
        sensorConfigurationFile.close()
        return configuredSensors

    def __findCurrentSensorName__(self, sensorId):
        matchingSensorsConfiguration = filter(lambda knownSensor: knownSensor['id'] == sensorId, self.sensorConfiguration)
        currentSensorConfiguration = next(matchingSensorsConfiguration)
        return currentSensorConfiguration['name']

    def __appendNameToSensors__(self, sensors):
        namedSensors = []
        for sensor in sensors:
            filteredSensorConfigurations = filter(lambda c: c['id'] == sensor['id'], self.sensorConfiguration)
            configuration = next(filteredSensorConfigurations)
            sensor['name'] = configuration['name']
            namedSensors.append(sensor)

        return namedSensors

    def __parseSensorData__(self, sensor):
        humidity = sensor.value(const.TELLSTICK_HUMIDITY) if sensor.has_value(const.TELLSTICK_HUMIDITY) else None
        temperature = sensor.value(const.TELLSTICK_TEMPERATURE)

        if humidity is None:
            return {'id': sensor.id, 'temperature': float(temperature.value)}
        else:
            return {'id': sensor.id, 'temperature': float(temperature.value), 'humidity': float(humidity.value)}

    def __parseSensorsData__(self, sensors):
        parsedSensors = map(self.__parseSensorData__, sensors)
        namedSensors = self.__appendNameToSensors__(parsedSensors)
        return namedSensors

    def __filter_known_sensors__(self, sensors):
        knownSensorIds = map(lambda knownSensor: knownSensor['id'], self.sensorConfiguration)
        knownSensors = filter(lambda sensor: sensor.id in knownSensorIds, sensors)
        return knownSensors

    def list_sensors(self, sensors):
        knownSensors = self.__filter_known_sensors__(sensors)
        parsedSensorData = self.__parseSensorsData__(knownSensors)
        return json.dumps(parsedSensorData, ensure_ascii=False).encode('utf8')
