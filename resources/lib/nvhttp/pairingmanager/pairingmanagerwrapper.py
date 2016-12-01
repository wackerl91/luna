import importlib

from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class PairingManagerWrapper(AbstractPairingManager):
    def __init__(self, crypto_provider, config_helper, logger):
        # implementation will be lazy loaded when needed
        self._crypto_provider = crypto_provider
        self._config_helper = config_helper
        self._logger = logger
        self._pairing_manager = None

    def pair(self, request_service, server_info, dialog):
        if self._pairing_manager is None:
            self._load_pairing_manager()
        return self._pairing_manager.pair(request_service, server_info, dialog)

    def unpair(self, request_service, server_info):
        if self._pairing_manager is None:
            self._load_pairing_manager()
        return self._pairing_manager.unpair(request_service, server_info)

    def _load_pairing_manager(self):
        try:
            module = importlib.import_module('resources.lib.nvhttp.pairingmanager.advancedpairingmanager')
            class_name = 'AdvancedPairingManager'
        except ImportError, e:
            print 'Could not load advanced pairing manager. Reason: %r' % e
            module = importlib.import_module('resources.lib.nvhttp.pairingmanager.simplepairingmanager')
            class_name = 'SimplePairingManager'

        class_ = getattr(module, class_name)
        self._pairing_manager = class_(self._crypto_provider, self._config_helper, self._logger)
