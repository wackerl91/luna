from resources.lib.controller.basecontroller import BaseController, route
from resources.lib.views.settings import Settings


class SettingsController(BaseController):
    def __init__(self, core, settings_parser, logger):
        super(SettingsController, self).__init__()
        self.core = core
        self.settings_parser = settings_parser
        self.logger = logger
        self.window = None

    @route(name='index')
    def index_action(self):
        settings = self.settings_parser.get_settings()
        if not self.window:
            self.window = Settings(controller=self, settings=settings)
        self.window.doModal()

    def save(self, settings):
        for category in settings:
            for _, setting in category.settings.iteritems():
                new_value = setting.current_value
                if new_value != setting.default and new_value != self.core.get_setting(setting.setting_id) and new_value is not None:
                    if isinstance(new_value, bool):
                        setting.current_value = str(setting.current_value).lower()
                    self.logger.info("Setting '%s' changed value: %s -> %s."
                                     % (setting.setting_label,
                                        self.core.get_setting(setting.setting_id),
                                        new_value))
                    self.core.set_setting(setting.setting_id, str(setting.current_value))
        return
