class CoreMonitor:
    def __init__(self, config_helper, logger):
        self.config_helper = config_helper
        self.logger = logger

    def onSettingsChanged(self):
        self.logger.info('Settings change called')
        self.config_helper.configure()
