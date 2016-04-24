import os

from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider


class SimpleCryptoProvider(AbstractCryptoProvider):
    def __init__(self, config_helper):
        self.name = 'Simple'
        self.config_helper = config_helper

    def get_cert_path(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight/client.pem')

    def get_key_path(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight/key.pem')

    def get_key_dir(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight/')

    def get_pem_encoded_client_cert(self):
        raise NotImplementedError

    def get_client_cert(self):
        raise NotImplementedError

    def get_client_private_key(self):
        raise NotImplementedError
