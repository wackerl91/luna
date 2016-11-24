from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class ConnectionManager(object):
    def __init__(self, request_service, pairing_manager):
        self.request_service = request_service
        self.pairing_manager = pairing_manager

    def pair(self, dialog):
        message = ''
        server_info = self.request_service.get_server_info()
        if self.pairing_manager.get_pair_state(self.request_service,
                                               server_info) == AbstractPairingManager.STATE_PAIRED:
            message = 'Already paired.'
            pair_state = AbstractPairingManager.STATE_PAIRED
        else:
            if self.request_service.get_current_game(server_info) != 0:
                message = 'Host is currently in-game, please exit the game before pairing.'
                pair_state = AbstractPairingManager.STATE_FAILED
            else:
                pair_state = self.pairing_manager.pair(self.request_service, server_info, dialog)

                if pair_state == AbstractPairingManager.STATE_PIN_WRONG:
                    message = 'PIN wrong.'
                if pair_state == AbstractPairingManager.STATE_FAILED:
                    message = 'Pairing failed.'
                if pair_state == AbstractPairingManager.STATE_PAIRED:
                    message = 'Pairing successful.'

        return message, pair_state

    def unpair(self):
        try:
            server_info = self.request_service.get_server_info()
            if self.pairing_manager.get_pair_state(self.request_service,
                                                   server_info) == AbstractPairingManager.STATE_PAIRED:
                self.pairing_manager.unpair(self.request_service, server_info)
        except ValueError:
            # Unpairing a host needs to be fire and forget
            pass
