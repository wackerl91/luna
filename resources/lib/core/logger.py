from xbmcswift2 import Plugin


class Logger:

    def __init__(self, plugin):
        self.plugin = plugin  # type: Plugin

    def info(self, text):
        self.plugin.log.info(text)

    def debug(self, text):
        self.plugin.log.debug(text)

    def error(self, text):
        self.plugin.log.error(text)
