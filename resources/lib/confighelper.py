import ConfigParser
import os

conf = 'luna.conf'


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
        self.resolution_width = None
        self.resolution_height = None
        self.resolution = None
        self.framerate = None
        self.host_optimizations = None
        self.remote_optimizations = None
        self.local_audio = None
        self.enable_custom_bitrate = None
        self.bitrate = None
        self.packetsize = None
        self.enable_custom_input = None
        self.input_map = None
        self.input_device = None
        self.full_path = None

    def _configure(self, addon_path, binary_path=None, host_ip=None, enable_custom_res=False, resolution_width=None,
                   resolution_height=None, resolution=None,
                   framerate=None, graphics_optimizations=False, remote_optimizations=False, local_audio=False,
                   enable_custom_bitrate=False, bitrate=None, packetsize=None,
                   enable_custom_input=False, input_map=None, input_device=None, override_default_resolution=False):

        self.addon_path = addon_path
        self.binary_path = binary_path
        self.host_ip = host_ip
        self.enable_custom_res = enable_custom_res
        self.resolution_width = resolution_width,
        self.resolution_height = resolution_height,
        self.resolution = resolution
        self.framerate = framerate
        self.graphics_optimizations = graphics_optimizations
        self.remote_optimizations = remote_optimizations
        self.local_audio = local_audio
        self.enable_custom_bitrate = enable_custom_bitrate
        self.bitrate = bitrate
        self.packetsize = packetsize
        self.enable_custom_input = enable_custom_input
        self.input_map = input_map
        self.input_device = input_device
        self.override_default_resolution = override_default_resolution

        self.full_path = ''.join([self.addon_path, conf])

    def configure(self, settings_dict):

        """
        :type settings_dict: dict
        """
        self._configure(**settings_dict)

    def dump_conf(self):
        """
        This dumps the currently configured helper into a file moonlight can read
        """
        config = ConfigParser.ConfigParser()
        config.read(self.full_path)

        if 'General' not in config.sections():
            config.add_section('General')

        config.set('General', 'binpath', self.binary_path)
        config.set('General', 'address', self.host_ip)

        if not self.override_default_resolution:
            if config.has_option('General', 'height'):
                config.remove_option('General', 'height')
            if config.has_option('General', 'width'):
                config.remove_option('General', 'width')
        else:
            if self.enable_custom_res:
                config.set('General', 'width', int(self.resolution_width[0]))
                config.set('General', 'height', int(self.resolution_height[0]))

            else:
                if self.resolution == '1920x1080':
                    config.set('General', 'width', 1920)
                    config.set('General', 'height', 1080)
                if self.resolution == '1280x720':
                    config.set('General', 'width', 1280)
                    config.set('General', 'height', 720)

        config.set('General', 'fps', self.framerate)
        if self.enable_custom_bitrate:
            config.set('General', 'bitrate', int(self.bitrate) * 1000)
        else:
            config.set('General', 'bitrate', -1)

        if self.packetsize != 1024:
            config.set('General', 'packetsize', self.packetsize)
        else:
            config.set('General', 'packetsize', 1024)

        if self.enable_custom_input:
            if self.input_map != '':
                if config.has_option('General', '#mapping'):
                    config.remove_option('General', '#mapping')
                config.set('General', 'mapping', self.input_map)
            else:
                if config.has_option('General', 'mapping'):
                    config.remove_option('General', 'mapping')
                config.set('General', '#mapping')

            if self.input_device != '':
                if config.has_option('General', '#input'):
                    config.remove_option('General', '#input')
                config.set('General', 'input', self.input_device)
            else:
                if config.has_option('General', 'input'):
                    config.remove_option('General', 'input')
                config.set('General', '#input')
        else:
            if config.has_option('General', 'mapping'):
                config.remove_option('General', 'mapping')
            config.set('General', '#mapping')

            if config.has_option('General', 'input'):
                config.remove_option('General', 'input')
            config.set('General', '#input')

        config.set('General', 'sops', self.graphics_optimizations)
        config.set('General', 'remote', self.remote_optimizations)
        config.set('General', 'localaudio', self.local_audio)

        with open(self.full_path, 'wb') as configfile:
            config.write(configfile)

    def get_binary(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return config_map('General', cp)['binpath']

    def get_host(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return config_map('General', cp)['address']

    def check_for_config_file(self):
        return os.path.isfile(self.full_path)

    def get_section_setting(self, section, setting):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return config_map(section, cp)[setting]

    def get_config_path(self):
        return self.full_path
