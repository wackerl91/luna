from resources.lib.core.logger.abstractlogger import AbstractLogger


class EosLogger(AbstractLogger):
    def __init__(self, log_level):
        super(EosLogger, self).__init__(log_level)
        self.eos_helper = None

    def warning(self, channel, text):
        self._log('warning', channel, text)

    def error(self, channel, text):
        self._log('error', channel, text)

    def debug(self, channel, text):
        self._log('debug', channel, text)

    def info(self, channel, text):
        self._log('info', channel, text)

    def critical(self, channel, text):
        self._log('critical', channel, text)

    def set_helper(self, eos_helper):
        self.eos_helper = eos_helper

    def _log(self, level, channel, text):
        if self.eos_helper is not None and self.LEVELS[level] >= self.LEVELS[self.log_level]:
            self.eos_helper.log(level, channel, text)
