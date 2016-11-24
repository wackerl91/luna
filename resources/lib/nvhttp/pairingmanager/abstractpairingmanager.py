import random
from abc import ABCMeta, abstractmethod


class AbstractPairingManager(object):
    __metaclass__ = ABCMeta

    STATE_NOT_PAIRED = 0
    STATE_PAIRED = 1
    STATE_PIN_WRONG = 2
    STATE_FAILED = 3

    @abstractmethod
    def pair(self, request_service, server_info, dialog):
        pass

    def unpair(self, request_service, server_info):
        try:
            request_service.open_http_connection(
                request_service.base_url_http + '/unpair?' + request_service.build_uid_uuid_string(),
                True
            )
        except ValueError:
            # Unpairing a host needs to be fire and forget
            pass

    @staticmethod
    def get_pair_state(request_service, server_info):
        if request_service.get_xml_string(server_info, 'PairStatus') != '1':
            return AbstractPairingManager.STATE_NOT_PAIRED
        else:
            return AbstractPairingManager.STATE_PAIRED

    @staticmethod
    def generate_pin_string():
        return '%s%s%s%s' % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    @staticmethod
    def update_dialog(pin, dialog):
        pin_message = 'Please enter the PIN: %s' % pin
        dialog.update(0, pin_message)
