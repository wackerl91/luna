from resources.lib.di.component import Component
from resources.lib.di.requiredfeature import RequiredFeature


class Logger(Component):
    def __init__(self):
        self.plugin = RequiredFeature('plugin')

    def info(self, text):
        self.plugin.log.info(text)

    def debug(self, text):
        self.plugin.log.debug(text)

    def error(self, text):
        self.plugin.log.error(text)
