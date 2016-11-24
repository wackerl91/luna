from resources.lib.nvhttp.cryptoprovider.cryptoproviderwrapper import CryptoProviderWrapper


class CryptoProviderFactory(object):
    def __init__(self, host_context_service):
        self.host_context_service = host_context_service

    def create_crypto_provider(self, config_helper):
        crypto_provider = CryptoProviderWrapper(config_helper)
        crypto_provider.configure(self.host_context_service.get_current_context())

        return crypto_provider
