import os
import subprocess
import threading

import re
from xbmcswift2 import xbmc, xbmcaddon


def loop_lines(dialog, iterator):
    """
    :type dialog:   DialogProgress
    :type iterator: iterator
    """
    for line in iterator:
        dialog.update(0, line)


class MoonlightHelper:
    regex_connect = '(Connect to)'
    regex_moonlight = '(Moonlight Embedded)'
    regex_certificate_gen = '(Generating certificate...done)'
    regex_connection_failed = '(Can\'t connect to server)'

    def __init__(self, plugin, config_helper, logger):
        self.plugin = plugin
        self.config_helper = config_helper
        self.logger = logger
        self.internal_path = xbmcaddon.Addon().getAddonInfo('path')

    def create_ctrl_map(self, dialog, map_file):
        """
        :type dialog:   DialogProgress
        :type map_file: str
        """
        mapping_proc = subprocess.Popen(
                ['stdbuf', '-oL', self.config_helper.get_binary(), 'map', map_file, '-input',
                 self.plugin.get_setting('input_device', unicode)], stdout=subprocess.PIPE)

        lines_iterator = iter(mapping_proc.stdout.readline, b"")

        mapping_thread = threading.Thread(target=loop_lines, args=(dialog, lines_iterator))
        mapping_thread.start()

        success = False

        # TODO: Make a method or function from this
        while True:
            xbmc.sleep(1000)
            if not mapping_thread.isAlive():
                dialog.close()
                success = True
                break
            if dialog.iscanceled():
                mapping_proc.kill()
                dialog.close()
                success = False
                break

        if os.path.isfile(map_file) and success:

            return True
        else:

            return False

    def pair_host(self, dialog):
        """
        :type dialog: DialogProgress
        """
        self.logger.info('[MoonlightHelper] - Attempting to pair host: ' + self.plugin.get_setting('host', unicode))
        pairing_proc = subprocess.Popen(
                ['stdbuf', '-oL', self.config_helper.get_binary(), 'pair', self.plugin.get_setting('host', unicode)],
                stdout=subprocess.PIPE)

        lines_iterator = iter(pairing_proc.stdout.readline, b"")

        pairing_thread = threading.Thread(target=loop_lines, args=(dialog, lines_iterator))
        pairing_thread.start()

        success = False

        while True:
            xbmc.sleep(1000)
            if not pairing_thread.isAlive():
                success = True
                break
            if dialog.iscanceled():
                pairing_proc.kill()
                dialog.close()
                success = False
                break

        if success:
            dialog.update(0, 'Checking if pairing has been successful.')
            xbmc.sleep(1000)
            pairing_check = subprocess.Popen([self.config_helper.get_binary(), 'list', self.config_helper.get_host()],
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            last = ''

            while True:
                line = pairing_check.stdout.readline()
                err = pairing_check.stderr.readline()
                if not re.match(self.regex_moonlight, line) and not re.match(self.regex_connect, line):
                    if line != '':
                        last = line
                if err != '':
                    last = err
                if not line and not err:
                    break

            dialog.close()
            if last.lower().strip() != 'You must pair with the PC first'.lower().strip() and not re.match(self.regex_connection_failed, last):
                return True
        else:

            return False

    def launch_game(self, game_id):
        """
        :type game_id: str
        """
        self.config_helper.configure()
        subprocess.call([
            self.internal_path + '/resources/lib/launchscripts/osmc/launch-helper-osmc.sh',
            self.internal_path + '/resources/lib/launchscripts/osmc/launch.sh',
            self.internal_path + '/resources/lib/launchscripts/osmc/moonlight-heartbeat.sh',
            game_id,
            self.config_helper.get_config_path()
        ])

    def list_games(self):
        self.config_helper.configure()
        game_list = []
        list_proc = subprocess.Popen([self.config_helper.get_binary(), 'list', self.config_helper.get_host()],
                                     stdout=subprocess.PIPE)

        while True:
            line = list_proc.stdout.readline()
            if re.match(self.regex_certificate_gen, line):
                game_list.append('error')
                return game_list
            if not re.match(self.regex_moonlight, line) and not re.match(self.regex_connect, line):
                if line[3:] != '':
                    game_list.append(line[3:].strip())
            if not line:
                break

        return game_list
