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

    def save(self, settings):
        for category in settings:
            for _, setting in category.settings.iteritems():
                new_value = setting.current_value
                if new_value != setting.default and new_value is not None:
                    self.logger.info("Setting '%s' changed value: %s -> %s."
                                     % (setting.setting_label,
                                        self.addon.getSetting(setting.setting_id),
                                        new_value))
                    self.addon.setSetting(setting.setting_id, str(setting.current_value))
        return
