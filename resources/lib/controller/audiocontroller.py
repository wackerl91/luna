import xbmcgui


class AudioController(object):
    def __init__(self, audio_manager, config_helper, plugin):
        self.audio_manager = audio_manager
        self.config_helper = config_helper
        self.plugin = plugin

    def select_audio_device(self):
        print "Number of audio devices: " + str(len(self.audio_manager.devices))
        device_list = [dev.name for dev in self.audio_manager.devices]
        device_list.append('sysdefault')
        audio_device = xbmcgui.Dialog().select('Choose Audio Device', device_list)

        if audio_device != -1:
            device_name = device_list[audio_device]
            device = self.audio_manager.get_device_by_name(device_name)
            if device:
                self.plugin.set_setting('audio_device', device.handler)
                self.plugin.set_setting('audio_device_name', device.name)

        return
