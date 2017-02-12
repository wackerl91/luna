import xbmc

from resources.lib.core.logger.abstractlogger import AbstractLogger


class Logger(AbstractLogger):
    def debug(self, channel, text):
        xbmc.log(self._format(channel, text), xbmc.LOGDEBUG)

    def info(self, channel, text):
        xbmc.log(self._format(channel, text), xbmc.LOGNOTICE)

    def warning(self, channel, text):
        xbmc.log(self._format(channel, text), xbmc.LOGWARNING)

    def error(self, channel, text):
        xbmc.log(self._format(channel, text), xbmc.LOGERROR)

    def critical(self, channel, text):
        xbmc.log(self._format(channel, text), xbmc.LOGSEVERE)

    def _format(self, channel, text):
        text = str(text)
        return '[%s]: %s' % (channel, text)
