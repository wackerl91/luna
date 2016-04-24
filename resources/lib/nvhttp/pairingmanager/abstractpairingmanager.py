import random
from abc import ABCMeta, abstractmethod


class AbstractPairingManager(object):
    __metaclass__ = ABCMeta

    STATE_NOT_PAIRED = 0
    STATE_PAIRED = 1
    STATE_PIN_WRONG = 2
    STATE_FAILED = 3

    @abstractmethod
    def pair(self, nvhttp, server_info, pin):
        pass

    @abstractmethod
    def get_pair_state(self, nvhttp, server_info):
        pass

    @staticmethod
    def generate_pin_string():
        return '%s%s%s%s' % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
