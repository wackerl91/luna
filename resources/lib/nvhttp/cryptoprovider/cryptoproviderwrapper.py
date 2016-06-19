import importlib

from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider


class CryptoProviderWrapper(AbstractCryptoProvider):
    def __init__(self, config_helper, host=None):
        self._config_helper = config_helper
        self._host = host
        # implementation will be lazy loaded when needed
        self._crypto_provider = None

    def configure(self, host):
        self._host = host

    def get_key_path(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_key_path()

    def get_key_dir(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_key_dir()

    def get_cert_path(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_cert_path()

    def get_pem_encoded_client_cert(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_pem_encoded_client_cert()

    def get_client_cert(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_client_cert()

    def get_client_private_key(self):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.get_client_private_key()

    def extract_cert_signature(self, cert):
        if self._crypto_provider is None:
            self._load_crypto_provider()
        return self._crypto_provider.extract_cert_signature(cert)

    def _load_crypto_provider(self):
        try:
            module = importlib.import_module('resources.lib.nvhttp.cryptoprovider.advancedcryptoprovider')
            class_name = 'AdvancedCryptoProvider'
        except ImportError, e:
            print 'Could not load advanced crypto provider. Reason: %r' % e
            module = importlib.import_module('resources.lib.nvhttp.cryptoprovider.simplecryptoprovider')
            class_name = 'SimpleCryptoProvider'

        if self._host is None:
            raise ValueError('Crypto provider can\'t be loaded as it is not configured.')
        class_ = getattr(module, class_name)
        self._crypto_provider = class_(self._config_helper, self._host)


