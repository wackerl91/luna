from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.selectinput import SelectInput


class ControllerConfigurationController(BaseController):
    def __init__(self):
        super(ControllerConfigurationController, self).__init__()
        self.window = None

    @route(name='select')
    def select_action(self):
        self.window = SelectInput(controller=self, title='Select Input Device')
        self.window.doModal()
        del self.window
