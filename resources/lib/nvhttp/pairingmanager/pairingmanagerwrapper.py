import importlib

from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class PairingManagerWrapper(AbstractPairingManager):
    def __init__(self):
        # implementation will be lazy loaded when needed
        self._pairing_manager = None

    def pair(self, nvhttp, server_info, pin):
        if self._pairing_manager is None:
            self._load_pairing_manager()
        return self._pairing_manager.pair(nvhttp, server_info, pin)

    def get_pair_state(self, nvhttp, server_info):
        if self._pairing_manager is None:
            self._load_pairing_manager()
        return self._pairing_manager.get_pair_state(nvhttp, server_info)

    def _load_pairing_manager(self):
        try:
            module = importlib.import_module('resources.lib.nvhttp.pairingmanager.advancedpairingmanager')
            class_name = 'AdvancedPairingManager'
        except ImportError, e:
            print 'Could not load advanced pairing manager. Reason: %r' % e
            module = importlib.import_module('resources.lib.nvhttp.pairingmanager.simplepairingmanager')
            class_name = 'SimplePairingManager'

        class_ = getattr(module, class_name)
        self._pairing_manager = class_(RequiredFeature('crypto-provider'))
