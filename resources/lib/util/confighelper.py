import ConfigParser
import os

from resources.lib.di.requiredfeature import RequiredFeature

conf = 'luna.conf'


class ConfigHelper:
    plugin = RequiredFeature('plugin')
    logger = RequiredFeature('logger')

    def __init__(self):
        self._reset()

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

    def configure(self):
        binary_path = self._find_binary()

        if binary_path is None:
            raise ValueError('Moonlight binary could not be found.')

        settings = {
            'addon_path':                   self.plugin.storage_path,
            'binary_path':                  binary_path,
            'host_ip':                      self.plugin.get_setting('host', unicode),
            'enable_custom_res':            self.plugin.get_setting('enable_custom_res', bool),
            'resolution_width':             self.plugin.get_setting('resolution_width', str),
            'resolution_height':            self.plugin.get_setting('resolution_height', str),
            'resolution':                   self.plugin.get_setting('resolution', str),
            'framerate':                    self.plugin.get_setting('framerate', str),
            'graphics_optimizations':       self.plugin.get_setting('graphic_optimizations', bool),
            'remote_optimizations':         self.plugin.get_setting('remote_optimizations', bool),
            'local_audio':                  self.plugin.get_setting('local_audio', bool),
            'enable_custom_bitrate':        self.plugin.get_setting('enable_custom_bitrate', bool),
            'bitrate':                      self.plugin.get_setting('bitrate', int),
            'packetsize':                   self.plugin.get_setting('packetsize', int),
            'enable_custom_input':          self.plugin.get_setting('enable_custom_input', bool),
            'input_map':                    self.plugin.get_setting('input_map', str),
            'input_device':                 self.plugin.get_setting('input_device', str),
            'override_default_resolution':  self.plugin.get_setting('override_default_resolution', bool)
        }
        self._configure(**settings)

        self._dump_conf()

    def _dump_conf(self):
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
                config.set('General', 'mapping', self.input_map)
            else:
                if config.has_option('General', 'mapping'):
                    config.remove_option('General', 'mapping')

            if self.input_device != '':
                config.set('General', 'input', self.input_device)
            else:
                if config.has_option('General', 'input'):
                    config.remove_option('General', 'input')
        else:
            if config.has_option('General', 'mapping'):
                config.remove_option('General', 'mapping')

            if config.has_option('General', 'input'):
                config.remove_option('General', 'input')

        config.set('General', 'sops', self.graphics_optimizations)
        config.set('General', 'remote', self.remote_optimizations)
        config.set('General', 'localaudio', self.local_audio)

        with open(self.full_path, 'wb') as configfile:
            config.write(configfile)
        configfile.close()

        self.logger.info('[ConfigHelper] - Dumped config to disk.')

    def get_binary(self):
        cp = ConfigParser.ConfigParser()

        try:
            cp.read(self.full_path)

            self.logger.info(
                    '[ConfigHelper] - Successfully loaded config file > trying to access binary path now')

            return self._config_map('General', cp)['binpath']

        except:
            self.logger.info(
                    '[ConfigHelper] - Exception occurred while attempting to read config from disk >' +
                    ' looking for binary file and dumping config file again.')

            binary_path = self._find_binary()
            self.configure()

            return binary_path

    def get_host(self):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return self._config_map('General', cp)['address']

    def check_for_config_file(self):
        return os.path.isfile(self.full_path)

    def get_section_setting(self, section, setting):
        cp = ConfigParser.ConfigParser()
        cp.read(self.full_path)
        return self._config_map(section, cp)[setting]

    def get_config_path(self):
        return self.full_path

    @staticmethod
    def _find_binary():
        binary_locations = [
            '/usr/bin/moonlight',
            '/usr/local/bin/moonlight'
        ]

        for f in binary_locations:
            if os.path.isfile(f):
                return f

        return None

    @staticmethod
    def _config_map(section, parser):
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
