import xbmc


class CoreMonitor(xbmc.Monitor):
    def __init__(self, core, config_helper):
        super(CoreMonitor, self).__init__()
        self.core = core
        self.config_helper = config_helper

    def onSettingsChanged(self):
        self.core.logger.info('Settings change called')
        self.config_helper.configure()
