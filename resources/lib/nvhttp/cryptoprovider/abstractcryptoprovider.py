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

    @abstractmethod
    def get_client_cert(self):
        pass

    @abstractmethod
    def get_client_private_key(self):
        pass

    @abstractmethod
    def get_pem_encoded_client_cert(self):
        pass

    @abstractmethod
    def extract_cert_signature(self, cert):
        pass
