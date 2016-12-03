class InputManager(object):
    def __init__(self, repository):
        self.repository = repository

    def get_input_devices(self):
        return self.repository.get_input_devices()

    def add_input_device(self, device_id, device):
        self.repository.add_input_device(device_id, device)

    def remove_input_device(self, device_id):
        self.repository.remove_input_device(device_id)

    def update_input_device(self, device_id, device):
        self.repository.update_input_device(device_id, device)
