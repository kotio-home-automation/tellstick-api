import tellcore.constants as const
import json

def __parseDeviceData(device):
    cmd = device.last_sent_command(const.TELLSTICK_TURNON | const.TELLSTICK_TURNOFF | const.TELLSTICK_DIM)
    return {'id': device.id, 'name': device.name, 'switchedOn': cmd == const.TELLSTICK_TURNON}

def __getDevice(deviceId, devices):
    filteredDevices = filter(lambda d: d.id == deviceId, devices)
    return next(filteredDevices)

def __turn_on_device(deviceId, devices):
    device = __getDevice(deviceId, devices)
    device.turn_on()

def __turn_off_device(deviceId, devices):
    device = __getDevice(deviceId, devices)
    device.turn_off()

def turn_off(deviceIds, devices):
    for deviceId in deviceIds:
        __turn_off_device(deviceId, devices)

def turn_on(deviceIds, devices):
    for deviceId in deviceIds:
        __turn_on_device(deviceId, devices)

def list_devices(devices):
    allSwitchesData = map(__parseDeviceData, devices)
    return json.dumps(list(allSwitchesData), ensure_ascii=False).encode('utf8')
