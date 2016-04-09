from resources.lib.model.inputmap import InputMap
from resources.lib.util.stoppablethread import StoppableThread


class StoppableJSHandler(StoppableThread):
    def __init__(self, input_wrapper, input_map):
        self.input = input_wrapper
        self.input.build_controller_map()
        self.js_dev = None
        self.map = input_map
        StoppableThread.__init__(self)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        print 'Opened input device %s' % self.input.device
        self.js_dev = open(self.input.device, 'rb')
        while True:
            if self.stopped():
                self.cleanup()
                return
            self.input.capture_input_events(self.js_dev)

    def cleanup(self):
        self.js_dev.close()
        if self.map.status == InputMap.STATUS_DONE:
            self.map.write()
        return
