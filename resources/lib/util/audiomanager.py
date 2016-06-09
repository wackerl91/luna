import os
import re

from resources.lib.model.audiodevice import AudioDevice


class AudioManager(object):
    CARDS_REGEX = r'[ ]?(\d) \[\w+[ ]+\]: (\w+[-_]*\w+) - ((\w+[ ]?)+)'

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

            card = card_info[0][-2]
            dev = card_info[1][-2]
            name = card_info[5]

            device = AudioDevice()
            audio_id = audio_id.replace('-', ' ')

            if name[6:].replace(audio_id, '').strip() == '':
                device.name = audio_name.replace('\n', '')
            else:
                device.name = name[6:].replace('\n', '')

            device.handler = 'hw:%s,%s' % (card, dev)
            subdevices_info.append(device)

        return subdevices_info

    def get_device_by_name(self, name):
        for device in self.devices:
            if device.name == name:
                return device
