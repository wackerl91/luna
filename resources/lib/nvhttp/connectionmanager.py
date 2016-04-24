from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class ConnectionManager(object):
    def pair(self, dialog):
        message = ''
        nvhttp = RequiredFeature('nvhttp').request()
        server_info = nvhttp.get_server_info()
        print 'ConnectionManager Server Info: %s' % server_info
        if nvhttp.get_pair_state(server_info) == AbstractPairingManager.STATE_PAIRED:
            message = 'Already paired'
        else:
            if nvhttp.get_current_game(server_info) != 0:
                message = 'Host is currently in-game, please exit the game before pairing.'
            else:
                pin_str = AbstractPairingManager.generate_pin_string()
                # Display pin_str in UI Dialog
                print 'Please enter the PIN: %s' % pin_str
                pair_state = nvhttp.pair(server_info, pin_str)
                if pair_state == AbstractPairingManager.STATE_PIN_WRONG:
                    message = 'Pin wrong'
                if pair_state == AbstractPairingManager.STATE_FAILED:
                    message = 'Failed'
                if pair_state == AbstractPairingManager.STATE_PAIRED:
                    message = 'Success'

        return message
