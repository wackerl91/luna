import re
import subprocess
import threading

import xbmc
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


class SimplePairingManager(AbstractPairingManager):
    def __init__(self, crypto_provider):
        self.crypto_provider = crypto_provider
        self.config_helper = RequiredFeature('config-helper').request()
        self.logger = RequiredFeature('logger').request()

    def pair(self, nvhttp, server_info, dialog):
        self.logger.info('[MoonlightHelper] - Attempting to pair host: ' + self.config_helper.host_ip)
        pairing_proc = subprocess.Popen(
                ['stdbuf', '-oL', self.config_helper.get_binary(), 'pair', self.config_helper.host_ip],
                stdout=subprocess.PIPE)

        lines_iterator = iter(pairing_proc.stdout.readline, b"")

        pairing_thread = threading.Thread(target=self.loop_lines, args=(self.logger, lines_iterator, dialog))
        pairing_thread.start()

        while True:
            xbmc.sleep(1000)
            if not pairing_thread.isAlive():
                break

        new_server_info = nvhttp.get_server_info()
        if self.get_pair_state(nvhttp, new_server_info) == self.STATE_PAIRED:
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
