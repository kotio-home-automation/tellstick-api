import tellcore.constants as const
import json

def __parseDeviceData__(device):
    lastCommand = device.last_sent_command(const.TELLSTICK_TURNON | const.TELLSTICK_TURNOFF | const.TELLSTICK_DIM)
    return {'id': device.id, 'name': device.name, 'switchedOn': lastCommand == const.TELLSTICK_TURNON}

def __getDevice__(deviceId, devices):
    filteredDevices = filter(lambda d: d.id == deviceId, devices)
    return next(filteredDevices)

def __turn_on_device__(deviceId, devices):
    device = __getDevice__(deviceId, devices)
    device.turn_on()

def __turn_off_device__(deviceId, devices):
    device = __getDevice__(deviceId, devices)
    device.turn_off()

def turn_off(deviceIds, devices):
    for deviceId in deviceIds:
        __turn_off_device__(deviceId, devices)

def turn_on(deviceIds, devices):
    for deviceId in deviceIds:
        __turn_on_device__(deviceId, devices)

def list_devices(devices):
    individualDevices = filter(lambda d: d.type != const.TELLSTICK_TYPE_GROUP, devices)
    deviceGroups = filter(lambda d: d.type == const.TELLSTICK_TYPE_GROUP, devices)
    individualDevicesData = list(map(__parseDeviceData__, individualDevices))
    deviceGroupsData = list(map(__parseDeviceData__, deviceGroups))
    allDevicesData = {'devices': individualDevicesData, 'groups': deviceGroupsData}
    return json.dumps(allDevicesData, ensure_ascii=False).encode('utf8')
