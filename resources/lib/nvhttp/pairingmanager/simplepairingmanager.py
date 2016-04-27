import subprocess
import threading

import xbmc
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager


def loop_lines(logger, iterator):
    for line in iterator:
        logger.info(line)


class SimplePairingManager(AbstractPairingManager):
    def __init__(self, crypto_provider):
        self.crypto_provider = crypto_provider
        self.config_helper = RequiredFeature('config-helper').request()
        self.logger = RequiredFeature('logger').request()

    def pair(self, nvhttp, server_info, pin):
        self.logger.info('[MoonlightHelper] - Attempting to pair host: ' + self.config_helper.host_ip)
        pairing_proc = subprocess.Popen(
                ['stdbuf', '-oL', self.config_helper.get_binary(), 'pair', self.config_helper.host_ip],
                stdout=subprocess.PIPE)

        lines_iterator = iter(pairing_proc.stdout.readline, b"")

        pairing_thread = threading.Thread(target=loop_lines, args=(self.logger, lines_iterator))
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
