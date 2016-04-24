from resources.lib.nvhttp.abstractcryptoprovider import AbstractCryptoProvider


class SimpleCryptoProvider(AbstractCryptoProvider):
    def __init__(self, config_helper):
        self.name = 'Simple'
        self.config_helper = config_helper

    def get_cert_path(self):
        pass

    def get_key_path(self):
        pass

    def get_key_dir(self):
        pass

