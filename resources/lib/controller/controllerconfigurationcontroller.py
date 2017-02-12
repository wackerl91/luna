from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.selectinput import SelectInput


class ControllerConfigurationController(BaseController):
    def __init__(self, core, device_wrapper, input_manager, moonlight_helper):
        self.core = core
        self.device_wrapper = device_wrapper
        self.input_manager = input_manager
        self.moonlight_helper = moonlight_helper
        self.window = None

    @route(name='select')
    def select_action(self):
        self.window = SelectInput(controller=self,
                                  available_devices=self.device_wrapper.devices,
                                  input_devices=self.get_input_devices(),
                                  title='Select Input Device')
        self.window.doModal()
        del self.window

    def get_internal_path(self):
        return self.core.internal_path

    def get_active_skin(self):
        return self.core.get_active_skin()

    def get_string(self, string_id):
        return self.core.string(string_id)

    def get_input_devices(self):
        return self.input_manager.get_input_devices()

    def add_input_device(self, ctrl_id, device):
        self.input_manager.add_input_device(ctrl_id, device)

    def remove_input_device(self, ctrl_id):
        self.input_manager.remove_input_device(ctrl_id)

    def update_input_device(self, ctrl_id, device):
        self.input_manager.update_input_device(ctrl_id, device)

    def find_device_by_name(self, name):
        return self.device_wrapper.find_device_by_name(name)

    def create_mapping_for_device(self, device, file_path, dialog):
        return self.moonlight_helper.create_ctrl_map_new(dialog, file_path, device)
