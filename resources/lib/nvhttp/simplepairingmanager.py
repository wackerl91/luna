from resources.lib.nvhttp.abstractpairingmanager import AbstractPairingManager


class SimplePairingManager(AbstractPairingManager):
    def get_pair_state(self, nvhttp, server_info):
        super(SimplePairingManager, self).get_pair_state()

    def pair(self, nvhttp, server_info, pin):
        super(SimplePairingManager, self).pair()
