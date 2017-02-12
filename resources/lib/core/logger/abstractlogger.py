from abc import ABCMeta, abstractmethod


class AbstractLogger:
    __metaclass__ = ABCMeta

    LEVELS = {
        'debug': 0,
        'info': 1,
        'notice': 2,
        'warning': 3,
        'error': 4,
        'severe': 5,
        'fatal': 6
    }

    def __init__(self, log_level):
        self.log_level = log_level

    @abstractmethod
    def debug(self, channel, text):
        pass

    @abstractmethod
    def info(self, channel, text):
        pass

    @abstractmethod
    def warning(self, channel, text):
        pass

    @abstractmethod
    def error(self, channel, text):
        pass

    @abstractmethod
    def critical(self, channel, text):
        pass
