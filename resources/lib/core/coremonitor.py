from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature


class CoreMonitor(Component):
    logger = RequiredFeature('logger')
    config_helper = RequiredFeature('config-helper')

    def __init__(self):
        pass

    def onSettingsChanged(self):
        self.logger.info('Settings change called')
        self.config_helper.configure()
