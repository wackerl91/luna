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

    def configure(self, file_path, binary_path=None, host_ip=None, enable_custom_res=False, resolution=None, framerate=None,
                   host_optimizations=False, local_audio=False, enable_custom_bitrate=False,
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

    def dump_conf(self):
        config = ConfigParser.ConfigParser()
        config.read(self.full_path)
        existing_sections = config.sections()
        if 'PairedHosts' not in existing_sections:
            config.add_section('PairedHosts')
        config.set('PairedHosts', 'host1', self.host_ip)
        if 'General' not in existing_sections:
            config.add_section('General')
        config.set('General', 'binpath', self.binary_path)

        with open(self.full_path, 'wb') as configfile:
            config.write(configfile)

    def get_binary(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return config_map('General', cp)['binpath']

    def check_for_config_file(self):
        return os.path.isfile(self.full_path)
