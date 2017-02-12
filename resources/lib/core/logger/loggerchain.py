from resources.lib.core.logger.abstractlogger import AbstractLogger


class LoggerChain(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.logger_chain = []

    def debug(self, message):
        for logger in self.logger_chain:
            logger.debug(self.prefix, message)

    def info(self, message):
        for logger in self.logger_chain:
            logger.info(self.prefix, message)

    def warning(self, message):
        for logger in self.logger_chain:
            logger.warning(self.prefix, message)

    def error(self, message):
        for logger in self.logger_chain:
            logger.error(self.prefix, message)

    def critical(self, message):
        for logger in self.logger_chain:
            logger.critical(self.prefix, message)

    def append(self, loggers):
        for logger in loggers:
            self._append_logger(logger)

    def _append_logger(self, logger):
        if isinstance(logger, AbstractLogger):
            self.logger_chain.append(logger)
        else:
            raise AssertionError('Expected to receive an instance of AbstractLogger, got %s instead' % type(logger))
