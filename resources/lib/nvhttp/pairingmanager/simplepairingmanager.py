import re
import subprocess
import threading

import xbmc

from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class SimplePairingManager(AbstractPairingManager):
    def __init__(self, crypto_provider, config_helper, logger):
        self.crypto_provider = crypto_provider
        self.config_helper = config_helper
        self.logger = logger

    def pair(self, request_service, server_info, dialog):
        self.logger.info('Attempting to pair host: ' + request_service.host_ip)
        pairing_proc = subprocess.Popen(
            ['stdbuf', '-oL', self.config_helper.get_binary(), 'pair', request_service.host_ip,
             '--keydir', self.crypto_provider.get_key_dir()],
            stdout=subprocess.PIPE)

        lines_iterator = iter(pairing_proc.stdout.readline, b"")

        pairing_thread = threading.Thread(target=self.loop_lines, args=(self.logger, lines_iterator, dialog))
        pairing_thread.start()

        while True:
            xbmc.sleep(1000)
            if not pairing_thread.isAlive():
                break

        new_server_info = request_service.get_server_info()
        if self.get_pair_state(request_service, new_server_info) == self.STATE_PAIRED:
            return self.STATE_PAIRED
        else:
            return self.STATE_FAILED

    def loop_lines(self, logger, iterator, dialog):
        pin_regex = r'^Please enter the following PIN on the target PC: (\d{4})'
        for line in iterator:
            match = re.match(pin_regex, line)
            if match:
                self.update_dialog(match.group(1), dialog)
            logger.info(line)
