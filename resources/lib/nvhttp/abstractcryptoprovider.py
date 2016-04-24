from abc import ABCMeta, abstractmethod


class AbstractCryptoProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_cert_path(self):
        pass

    @abstractmethod
    def get_key_path(self):
        pass

    @abstractmethod
    def get_key_dir(self):
        pass
