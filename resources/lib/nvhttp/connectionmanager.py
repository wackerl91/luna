from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class ConnectionManager(object):
    def pair(self, dialog, host):
        message = ''
        nvhttp = RequiredFeature('nvhttp').request()
        nvhttp.configure_from_host_details(host)
        server_info = nvhttp.get_server_info()
        if nvhttp.get_pair_state(server_info) == AbstractPairingManager.STATE_PAIRED:
            message = 'Already paired.'
            pair_state = AbstractPairingManager.STATE_PAIRED
        else:
            if nvhttp.get_current_game(server_info) != 0:
                message = 'Host is currently in-game, please exit the game before pairing.'
                pair_state = AbstractPairingManager.STATE_FAILED
            else:
                pin_str = AbstractPairingManager.generate_pin_string()
                pin_message = 'Please enter the PIN: %s' % pin_str
                dialog.update(0, pin_message)
                pair_state = nvhttp.pair(server_info, pin_str)

                if pair_state == AbstractPairingManager.STATE_PIN_WRONG:
                    message = 'PIN wrong.'
                if pair_state == AbstractPairingManager.STATE_FAILED:
                    message = 'Pairing failed.'
                if pair_state == AbstractPairingManager.STATE_PAIRED:
                    message = 'Pairing successful.'

        return message, pair_state
