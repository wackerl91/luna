import os
import subprocess
import threading

from xbmcswift2 import Plugin, xbmc, xbmcaddon
from xbmcgui import DialogProgress

from resources.lib.confighelper import ConfigHelper


def loop_lines(dialog, iterator):
    """
    :type dialog:   DialogProgress
    :type iterator: iterator
    """
    for line in iterator:
        dialog.update(0, line)


class MoonlightHelper:
    def __init__(self, helper):
        """
        :type helper: ConfigHelper
        """
        self.config_helper = helper
        self.plugin = Plugin('script.luna')
        self.internal_path = xbmcaddon.Addon().getAddonInfo('path')

    def create_ctrl_map(self, dialog, map_file):
        """
        :type dialog:   DialogProgress
        :type map_file: str
        """
        mapping_proc = subprocess.Popen(
                [self.config_helper.get_binary(), 'map', map_file, '-input',
                 self.plugin.get_setting('input_device', unicode)], stdout=subprocess.PIPE, bufsize=1)

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
        pairing_proc = subprocess.Popen([self.config_helper.get_binary(), 'pair', self.config_helper.get_host()],
                                        stdout=subprocess.PIPE, bufsize=1)
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
            dialog.update(0, 'Checking if pairing has benn successful.')
            xbmc.sleep(1000)
            pairing_check = subprocess.Popen([self.config_helper.get_binary(), 'list', self.config_helper.get_host()],
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            last = ''

            while True:
                line = pairing_check.stdout.readline()
                err = pairing_check.stderr.readline()
                if line != '':
                    last = line
                if err != '':
                    last = err
                if not line and not err:
                    break

            dialog.close()
            if last.lower().strip() != 'You must pair with the PC first'.lower().strip():
                return True
        else:

            return False

    def launch_game(self, game_id):
        """
        :type game_id: str
        """
        self.config_helper.configure()
        subprocess.call([
            self.internal_path + '/resources/lib/launch-helper-osmc.sh',
            self.internal_path + '/resources/lib/launch.sh',
            self.internal_path + '/resources/lib/moonlight-heartbeat.sh',
            game_id,
            self.config_helper.get_config_path()
        ])
