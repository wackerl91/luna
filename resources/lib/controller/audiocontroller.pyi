from resources.lib.util.audiomanager import AudioManager
from resources.lib.core.corefunctions import Core
from resources.lib.util.confighelper import ConfigHelper


class AudioController:
    audio_manager = ... # type: AudioManager
    config_helper = ... # type: ConfigHelper
    def __init__(self, core: Core, audio_manager: AudioManager, config_helper: ConfigHelper):
        self.core = Core
        self.audio_manager = AudioManager
        self.config_helper = ConfigHelper
        ...
    def select_audio_device(self) -> None: ...
