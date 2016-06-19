import os

from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider


class SimpleCryptoProvider(AbstractCryptoProvider):
    def __init__(self, config_helper, host):
        self.config_helper = config_helper
        self.host = host

    def get_cert_path(self):
        return os.path.join(self.get_key_base_path(), self.host.uuid, 'client.pem')

    def get_key_path(self):
        return os.path.join(self.get_key_base_path(), self.host.uuid, 'key.pem')

    def get_key_dir(self):
        return os.path.join(self.get_key_base_path(), self.host.uuid)

    def get_pem_encoded_client_cert(self):
        raise NotImplementedError

    def get_client_cert(self):
        raise NotImplementedError

    def get_client_private_key(self):
        raise NotImplementedError

    def extract_cert_signature(self, cert):
        raise NotImplementedError

