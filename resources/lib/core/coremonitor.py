from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature


class CoreMonitor(Component):
    def __init__(self):
        self.core = RequiredFeature('core')
        self.config_helper = RequiredFeature('config-helper')

    def onSettingsChanged(self):
        self.core.logger.info('Settings change called')
        self.config_helper.configure()
