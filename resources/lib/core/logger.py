from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature


class Logger(Component):
    plugin = RequiredFeature('plugin')

    def __init__(self):
        pass

    def info(self, text):
        self.plugin.log.info(text)

    def debug(self, text):
        self.plugin.log.debug(text)

    def error(self, text):
        self.plugin.log.error(text)
