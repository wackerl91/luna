from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class SimplePairingManager(AbstractPairingManager):
    def __init__(self, crypto_provider):
        self.crypto_provider = crypto_provider

    def get_pair_state(self, nvhttp, server_info):
        # super(SimplePairingManager, self).get_pair_state()
        return False

    def pair(self, nvhttp, server_info, pin):
        super(SimplePairingManager, self).pair()
