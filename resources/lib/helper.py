import ConfigParser
import os

conf = '/resources/luna.ini'


def config_map(section, parser):
    """

    :param section: string
    :type parser: ConfigParser.ConfigParser
    """
    dict1 = {}
    options = parser.options(section)
    for option in options:
        try:
            dict1[option] = parser.get(section, option)
        except:
            dict1[option] = None
    return dict1


class ConfigHelper:
    def __init__(self, *args, **kwargs):
        self._reset()
        if args or kwargs:
            self.configure(*args, **kwargs)

    def _reset(self):
        self.file_path = None
        self.binary_path = None
        self.host_ip = None
        self.enable_custom_res = None
        self.resolution = None
        self.framerate = None
        self.host_optimizations = None
        self.local_audio = None
        self.enable_custom_bitrate = None
        self.enable_custom_input = None
        self.input_map = None
        self.input_device = None
        self.full_path = None

    def _configure(self, file_path, binary_path=None, host_ip=None, enable_custom_res=False, resolution=None,
                  framerate=None, host_optimizations=False, local_audio=False, enable_custom_bitrate=False,
                  enable_custom_input=False, input_map=None, input_device=None):
        self.file_path = file_path
        self.binary_path = binary_path
        self.host_ip = host_ip
        self.enable_custom_res = enable_custom_res
        self.resolution = resolution
        self.framerate = framerate
        self.host_optimizations = host_optimizations
        self.local_audio = local_audio
        self.enable_custom_bitrate = enable_custom_bitrate
        self.enable_custom_input = enable_custom_input
        self.input_map = input_map
        self.input_device = input_device

        self.full_path = ''.join([self.file_path, conf])

    def configure(self, file_path, binary_path=None, host_ip=None, enable_custom_res=False, resolution=None,
                  framerate=None, host_optimizations=False, local_audio=False, enable_custom_bitrate=False,
                  enable_custom_input=False, input_map=None, input_device=None):

        self._configure(
            file_path,
            binary_path,
            host_ip,
            enable_custom_res,
            resolution,
            framerate,
            host_optimizations,
            local_audio,
            enable_custom_bitrate,
            enable_custom_input,
            input_map,
            input_device
        )

    def dump_conf(self):
        config = ConfigParser.ConfigParser()
        config.read(self.full_path)

        if 'General' not in config.sections():
            config.add_section('General')

        config.set('General', 'binpath', self.binary_path)
        config.set('General', 'host', self.host_ip)
        config.set('General', 'enable_custom_resolution', self.enable_custom_res)
        config.set('General', 'resolution', self.resolution),
        config.set('General', 'framerate', self.framerate),
        config.set('General', 'host_optimizations', self.host_optimizations),
        config.set('General', 'local_audio', self.local_audio),
        config.set('General', 'enable_custom_bitrate', self.enable_custom_bitrate),
        config.set('General', 'enable_custom_input', self.enable_custom_input),
        config.set('General', 'input_map', self.input_map),
        config.set('General', 'input_device', self.input_device)

        with open(self.full_path, 'wb') as configfile:
            config.write(configfile)

    def get_binary(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return config_map('General', cp)['binpath']

    def check_for_config_file(self):
        return os.path.isfile(self.full_path)
