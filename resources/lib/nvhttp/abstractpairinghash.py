from abc import ABCMeta, abstractmethod


class AbstractPairingHash:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_hash_length(self):
        pass

    @abstractmethod
    def hash_data(self, data):
        pass
