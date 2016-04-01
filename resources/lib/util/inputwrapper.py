import array
import os
import struct

from fcntl import ioctl

from resources.lib.model.inputmap import InputMap

axis_names = {
    0x00: 'x',
    0x01: 'y',
    0x02: 'z',
    0x03: 'rx',
    0x04: 'ry',
    0x05: 'rz',
    0x06: 'trottle',
    0x07: 'rudder',
    0x08: 'wheel',
    0x09: 'gas',
    0x0a: 'brake',
    0x10: 'hat0x',
    0x11: 'hat0y',
    0x12: 'hat1x',
    0x13: 'hat1y',
    0x14: 'hat2x',
    0x15: 'hat2y',
    0x16: 'hat3x',
    0x17: 'hat3y',
    0x18: 'pressure',
    0x19: 'distance',
    0x1a: 'tilt_x',
    0x1b: 'tilt_y',
    0x1c: 'tool_width',
    0x20: 'volume',
    0x28: 'misc',
}

button_names = {
    0x120: 'trigger',
    0x121: 'thumb',
    0x122: 'thumb2',
    0x123: 'top',
    0x124: 'top2',
    0x125: 'pinkie',
    0x126: 'base',
    0x127: 'base2',
    0x128: 'base3',
    0x129: 'base4',
    0x12a: 'base5',
    0x12b: 'base6',
    0x12f: 'dead',
    0x130: 'a',
    0x131: 'b',
    0x132: 'c',
    0x133: 'x',
    0x134: 'y',
    0x135: 'z',
    0x136: 'tl',
    0x137: 'tr',
    0x138: 'tl2',
    0x139: 'tr2',
    0x13a: 'select',
    0x13b: 'start',
    0x13c: 'mode',
    0x13d: 'thumbl',
    0x13e: 'thumbr',

    0x220: 'dpad_up',
    0x221: 'dpad_down',
    0x222: 'dpad_left',
    0x223: 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0: 'dpad_left',
    0x2c1: 'dpad_right',
    0x2c2: 'dpad_up',
    0x2c3: 'dpad_down',
}


class InputWrapper:
    def __init__(self, device, device_name, input_queue, input_map):
        self.device = device
        self.device_name = device_name
        self.axis_states = {}
        self.button_states = {}
        self.num_buttons = 0
        self.num_axes = 0
        self.btn_map = []
        self.axis_map = []
        self.reverse_btn_map = {}
        self.reverse_axis_map = {}
        self.input_queue = input_queue
        self.input_map = input_map
        if not os.path.exists(device):
            raise OSError('No such input device %s' % device)

    @staticmethod
    def list_all_devices():
        devices = {}
        for _dev in os.listdir('/dev/input'):
            if _dev.startswith('js'):
                js_dev = open(os.path.join('/dev/input', _dev), 'rb')
                buf = array.array('c', ['\0'] * 64)
                ioctl(js_dev,  0x80006a13 + (0x10000 * len(buf)), buf)
                js_name = buf.tostring()
                devices[_dev] = js_name
                print _dev
                print type(js_name)
                # print 'Added device %s / %s to list' % (_dev, js_name)
        return devices

    def build_controller_map(self):
        js_dev = open(self.device, 'rb')

        buf = array.array('B', [0])
        ioctl(js_dev, 0x80016a11, buf)
        self.num_axes = buf[0]
        print self.num_axes

        buf = array.array('B', [0])
        ioctl(js_dev, 0x80016a12, buf)
        self.num_buttons = buf[0]
        print self.num_buttons

        buf = array.array('B', [0] * 0x40)
        ioctl(js_dev, 0x80406a32, buf)
        for axis in buf[:self.num_axes]:
            axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0
            self.reverse_axis_map[axis_name] = axis

        buf = array.array('H', [0] * 200)
        ioctl(js_dev, 0x80406a34, buf)
        for btn in buf[:self.num_buttons]:
            btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.btn_map.append(btn_name)
            self.button_states[btn_name] = 0
            self.reverse_btn_map[btn_name] = btn

        js_dev.close()

    def capture_input_events(self, js_dev):
        if self.input_map.status == InputMap.STATUS_PENDING:
            evbuf = js_dev.read(8)

            if evbuf:
                time_stamp, value, input_type, number = struct.unpack('IhBB', evbuf)

                if input_type & 0x80:
                    pass

                if input_type & 0x01:
                    button = self.btn_map[number]
                    if button:
                        btn_number = self.reverse_btn_map[button]
                        if value:
                            self.input_queue.put((btn_number, button, value, 'btn'))

                if input_type & 0x02:
                    axis = self.axis_map[number]
                    if axis:
                        axis_number = self.reverse_axis_map[axis]
                        fvalue = value / 32767.0
                        if abs(fvalue) == 1:
                            self.input_queue.put((axis_number, axis, fvalue, 'ax'))
