from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.views.settings import Settings


class SettingsController(BaseController):
    def __init__(self):
        super(SettingsController, self).__init__()
        self.addon = RequiredFeature('addon').request()
        self.logger = RequiredFeature('logger').request()
        self.window = None

    @route(name='index')
    def index_action(self):
        settings_parser = RequiredFeature('settings-parser').request()
        settings_parser.get_settings()
        window = Settings(controller=self)
        window.doModal()
        del window
