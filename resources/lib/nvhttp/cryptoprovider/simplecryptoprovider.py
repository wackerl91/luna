import os

from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider


class SimpleCryptoProvider(AbstractCryptoProvider):
    def __init__(self, host_context_service, config_helper):
        super(SimpleCryptoProvider, self).__init__(host_context_service)
        self.config_helper = config_helper

    def get_cert_path(self):
        super(SimpleCryptoProvider, self).get_cert_path()
        return os.path.join(self.get_key_base_path(), self._current_host.uuid, 'client.pem')

    def get_key_path(self):
        super(SimpleCryptoProvider, self).get_key_path()
        return os.path.join(self.get_key_base_path(), self._current_host.uuid, 'key.pem')

    def get_key_dir(self):
        super(SimpleCryptoProvider, self).get_key_dir()
        return os.path.join(self.get_key_base_path(), self._current_host.uuid)

    def get_pem_encoded_client_cert(self):
        raise NotImplementedError

    def get_client_cert(self):
        raise NotImplementedError

    def get_client_private_key(self):
        raise NotImplementedError

    def extract_cert_signature(self, cert):
        raise NotImplementedError

