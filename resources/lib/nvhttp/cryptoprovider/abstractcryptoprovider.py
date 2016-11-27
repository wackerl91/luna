import os
from abc import ABCMeta, abstractmethod


class AbstractCryptoProvider(object):
    __metaclass__ = ABCMeta

    def __init__(self, host_context_service):
        self.host_context_service = host_context_service
        self._current_host = None

    @abstractmethod
    def get_cert_path(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def get_key_path(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def get_key_dir(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def get_client_cert(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def get_client_private_key(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def get_pem_encoded_client_cert(self):
        self._current_host = self.host_context_service.get_current_host()

    @abstractmethod
    def extract_cert_signature(self, cert):
        self._current_host = self.host_context_service.get_current_host()

    @staticmethod
    def get_key_base_path():
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight')
