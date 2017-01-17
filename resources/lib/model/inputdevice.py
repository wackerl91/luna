import os


class InputDevice:
    def __init__(self):
        self.name = None
        self.handlers = []
        self.mapping = None

    def is_kbd(self):
        return False
        # found_kbd = False
        # found_js = False
        # for _handler in self.handlers:
        #     if _handler[:-1] == 'kbd':
        #         found_kbd = True
        #     if _handler[:-1] == 'js':
        #         found_js = True
        #
        # return found_kbd and not found_js

    def is_mouse(self):
        return False
        # found_mouse = False
        # found_js = False
        # for _handler in self.handlers:
        #     if _handler[:-1] == 'mouse':
        #         found_mouse = True
        #     if _handler[:-1] == 'js':
        #         found_js = True
        #
        # return found_mouse and not found_js

    def is_none_device(self):
        return self.name == 'None (Disabled)'

    def get_evdev(self):
        for handler in self.handlers:
            if handler[:-1] == 'event':
                return os.path.join('/dev/input', handler)
