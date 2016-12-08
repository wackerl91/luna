import os
import re

import xbmc
from resources.lib.model.audiodevice import AudioDevice


class AudioManager(object):
    CARDS_REGEX = r'[ ]?(\d) \[\w+[ ]*\]: (\w+[-_]*\w+) - ((\w+[ ]?)+)'

    def __init__(self):
        self.devices = []
        self.init_devices()

    def init_devices(self):
        cards_file = '/proc/asound/cards'

        with open(cards_file) as f:
            cards = f.readlines()
            f.close()

        for card in cards:
            match = re.match(self.CARDS_REGEX, card)
            if match:
                curr_idx = match.group(1)
                curr_id = match.group(2)
                curr_name = match.group(3)
                for device in self.get_card_info(curr_idx, curr_id, curr_name):
                    self.devices.append(device)

    def get_card_info(self, idx, audio_id, audio_name):
        card_info_dir = os.path.abspath(os.path.join('/proc/asound/', 'card%s' % idx))
        subdevices = [x for x in next(os.walk(card_info_dir))]

        subdevices_info = []

        for subdevice in subdevices[1]:
            card_info_file = os.path.join(subdevices[0], subdevice, 'info')
            if not os.path.isfile(card_info_file):
                return
            with open(card_info_file) as f:
                card_info = f.readlines()
                f.close()

            device = AudioDevice()
            device.original_name = audio_name

            for entry in card_info:
                entry = entry.replace('\n', '')
                entry = entry.strip()
                components = entry.split(':')
                # components[0] is the key, [1] the value
                setattr(device, components[0].strip(), components[1].strip())

            device.handler = 'hw:%s,%s' % (device.card, device.device)

            if device.stream is None or device.stream == 'PLAYBACK':
                subdevices_info.append(device)

        return subdevices_info

    def get_device_by_name(self, name):
        for device in self.devices:
            if device.get_name() == name:
                return device
