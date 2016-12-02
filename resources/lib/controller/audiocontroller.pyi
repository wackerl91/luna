from xbmcaddon import Addon

from resources.lib.util.audiomanager import AudioManager
from resources.lib.util.confighelper import ConfigHelper


class AudioController:
    audio_manager = ... # type: AudioManager
    config_helper = ... # type: ConfigHelper
    def __init__(self, audio_manager: AudioManager, config_helper: ConfigHelper, addon: Addon):
        self.audio_manager = AudioManager
        self.config_helper = ConfigHelper
        self.addon = Addon
        ...
    def select_audio_device(self) -> None: ...
