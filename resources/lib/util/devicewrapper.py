import os

import re

from resources.lib.model.inputdevice import InputDevice


class DeviceWrapper:
    def __init__(self):
        self.devices = []
        self.init_devices()

    def init_devices(self):
        input_bus = '/proc/bus/input/devices'
        if not os.path.exists(input_bus):
            message = 'Input bus (%s) could not be accessed.' % input_bus
            raise OSError(message)
        with open(input_bus) as f:
            device = None
            for line in f.readlines():
                if line.startswith('I:'):
                    device = InputDevice()
                if line.startswith('N:'):
                    print line[9:-2]
                    name = line[9:-2]
                    for _dev in self.devices:
                        if _dev.name == name:
                            print 'found duplicate entry'
                            name += ' #2'
                    device.name = name
                if line.startswith('H:'):
                    handlers = line[12:].split()
                    for handler in handlers:
                        device.handlers.append(handler)
                if re.match('\n', line):
                    if device:
                        self.devices.append(device)
            for _dev in self.devices:
                if _dev.name == 'lircd':
                    self.devices.remove(_dev)

    def find_device_by_name(self, name):
        for device in self.devices:
            if device.name == name:
                return device
        return None

    def find_device_by_js(self, js):
        for device in self.devices:
            if js in device.handlers:
                return device
        return None
