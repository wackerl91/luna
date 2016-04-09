import os


class InputDevice:
    def __init__(self):
        self.name = None
        self.handlers = []
        self.mapping = None

    def is_kbd(self):
        return 'kbd' in self.handlers

    def is_mouse(self):
        for _handler in self.handlers:
            if _handler[:-1] == 'mouse':
                return True

    def is_none_device(self):
        return self.name == 'None (Disabled)'

    def get_evdev(self):
        for handler in self.handlers:
            if handler[:-1] == 'event':
                return os.path.join('/dev/input', handler)
