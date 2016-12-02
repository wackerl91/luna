import xbmcgui
from resources.lib.controller.basecontroller import BaseController, route


class AudioController(BaseController):
    def __init__(self, audio_manager, config_helper, addon):
        self.audio_manager = audio_manager
        self.config_helper = config_helper
        self.addon = addon

    @route(name="select")
    def select_audio_device(self):
        device_list = [dev.name for dev in self.audio_manager.devices]
        device_list.append('sysdefault')
        audio_device = xbmcgui.Dialog().select('Choose Audio Device', device_list)

        if audio_device != -1:
            device_name = device_list[audio_device]
            device = self.audio_manager.get_device_by_name(device_name)
            if device:
                self.addon.setSetting('audio_device', device.handler)
                self.addon.setSetting('audio_device_name', device.name)

        return
