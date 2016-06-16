import random
from abc import ABCMeta, abstractmethod


class AbstractPairingManager(object):
    __metaclass__ = ABCMeta

    STATE_NOT_PAIRED = 0
    STATE_PAIRED = 1
    STATE_PIN_WRONG = 2
    STATE_FAILED = 3

    @abstractmethod
    def pair(self, nvhttp, server_info, dialog):
        pass

    @staticmethod
    def get_pair_state(nvhttp, server_info):
        if nvhttp.get_xml_string(server_info, 'PairStatus') != '1':
            return AbstractPairingManager.STATE_NOT_PAIRED
        else:
            return AbstractPairingManager.STATE_PAIRED

    @staticmethod
    def generate_pin_string():
        return '%s%s%s%s' % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    @staticmethod
    def update_dialog(pin, dialog):
        pin_message = 'Please enter the PIN: %s' % pin
        dialog.update(0, pin_message)
