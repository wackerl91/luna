import xbmc


class Logger:
    def __init__(self, prefix):
        self.prefix = prefix

    def debug(self, text):
        xbmc.log(self._format(text), xbmc.LOGDEBUG)

    def info(self, text):
        xbmc.log(self._format(text), xbmc.LOGNOTICE)

    def warning(self, text):
        xbmc.log(self._format(text), xbmc.LOGWARNING)

    def error(self, text):
        xbmc.log(self._format(text), xbmc.LOGERROR)

    def critical(self, text):
        xbmc.log(self._format(text), xbmc.LOGSEVERE)

    def _format(self, text):
        text = str(text)
        return '[%s]: %s' % (self.prefix, text)
