class InputRepository(object):
    def __init__(self, core, logger):
        self.storage = core.get_storage('input_storage')
        self.logger = logger

    def get_input_devices(self):
        return dict((key, value[0]) for (key, value) in self.storage.raw_dict().iteritems())

    def add_input_device(self, device_id, device, flush=True):
        if device_id not in self.storage.keys():
            self.storage[device_id] = device

            if flush:
                self.storage.sync()
        else:
            self.logger.warning("Device ID '%s' already present, will not be replaced" % device_id)

    def remove_input_device(self, device_id, flush=True):
        if device_id in self.storage.keys():
            del self.storage[device_id]

            if flush:
                self.storage.sync()
        else:
            self.logger.warning("Attempted to remove non-existent device: '%s'" % device_id)

    def update_input_device(self, device_id, device, flush=True):
        if device_id in self.storage.keys():
            self.storage[device_id] = device

            if flush:
                self.storage.sync()
        else:
            self.logger.warning("Attempted to update non-existent device: '%s'" % device_id)

    def clear(self):
        self.logger.info("Clearing Input Storage")
        self.storage.clear()
        self.storage.sync()
